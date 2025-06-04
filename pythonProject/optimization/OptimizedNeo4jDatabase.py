"""
Tối ưu hóa Knowledge Graph (Neo4j) để truy xuất nhanh hơn
Cải tiến:
1. Query optimization và indexing
2. Connection pooling
3. Caching strategies
4. Parallel query execution
5. Memory-efficient result processing
"""

import asyncio
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import hashlib
import json
from neo4j import GraphDatabase, Session
from neo4j.exceptions import ServiceUnavailable
from dataclasses import dataclass
import threading

@dataclass
class QueryResult:
    """Kết quả query với metadata"""
    data: List[Dict]
    execution_time: float
    cache_hit: bool = False

class QueryCache:
    """Cache cho Neo4j queries"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 1800):  # 30 minutes
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.lock = threading.RLock()
        
    def _get_hash(self, query: str, params: Dict = None) -> str:
        """Tạo hash cho query và parameters"""
        query_str = query + str(sorted((params or {}).items()))
        return hashlib.md5(query_str.encode()).hexdigest()
    
    def get(self, query: str, params: Dict = None) -> Optional[List[Dict]]:
        """Lấy kết quả từ cache"""
        with self.lock:
            key = self._get_hash(query, params)
            current_time = time.time()
            
            if key in self.cache:
                result, cache_time = self.cache[key]
                if current_time - cache_time < self.ttl_seconds:
                    self.access_times[key] = current_time
                    return result
                else:
                    # Expired entry
                    del self.cache[key]
                    del self.access_times[key]
            
            return None
    
    def set(self, query: str, result: List[Dict], params: Dict = None):
        """Lưu kết quả vào cache"""
        with self.lock:
            key = self._get_hash(query, params)
            current_time = time.time()
            
            # LRU eviction
            if len(self.cache) >= self.max_size:
                oldest_key = min(self.access_times.keys(), 
                               key=lambda k: self.access_times[k])
                del self.cache[oldest_key]
                del self.access_times[oldest_key]
            
            self.cache[key] = (result, current_time)
            self.access_times[key] = current_time

class OptimizedNeo4jDatabase:
    """Neo4j database tối ưu hóa với connection pooling và caching"""
    
    def __init__(self, uri: str, user: str, password: str, 
                 max_connection_pool_size: int = 50,
                 max_connection_lifetime: int = 3600,
                 connection_acquisition_timeout: int = 60):
          # Cấu hình connection pool tối ưu
        self.driver = GraphDatabase.driver(
            uri, 
            auth=(user, password),
            max_connection_pool_size=max_connection_pool_size,
            max_connection_lifetime=max_connection_lifetime,
            connection_acquisition_timeout=connection_acquisition_timeout,
            keep_alive=True,
            initial_retry_delay=1.0,
            retry_delay_multiplier=2.0,
            retry_delay_jitter_factor=0.2
        )
        
        # Cache và performance tracking
        self.query_cache = QueryCache()
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.metrics = {
            'query_count': 0,
            'cache_hits': 0,
            'avg_execution_time': 0,
            'query_times': []
        }
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        # Tạo indexes tối ưu
        self._create_optimized_indexes()
        
    def _create_optimized_indexes(self):
        """Tạo các indexes tối ưu cho performance"""
        indexes_queries = [
            # Index cho node names
            "CREATE INDEX entity_name_index IF NOT EXISTS FOR (n:Part) ON (n.name)",
            "CREATE INDEX section_name_index IF NOT EXISTS FOR (n:Section) ON (n.name)",
            "CREATE INDEX article_name_index IF NOT EXISTS FOR (n:Article) ON (n.name)",
            
            # Composite indexes cho queries phổ biến
            "CREATE INDEX part_section_composite IF NOT EXISTS FOR (n:Part) ON (n.name, n.type)",
              # Full-text search indexes
            "CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS FOR (n:Part|Section|Article) ON EACH [n.name]"
            
            # Note: Relationship indexes have different syntax and are not always supported
            # in all Neo4j versions, so we'll skip them for now
        ]
        
        for query in indexes_queries:
            try:
                with self.driver.session() as session:
                    session.run(query)
                self.logger.info(f"Created index: {query}")
            except Exception as e:
                self.logger.warning(f"Index creation failed (may already exist): {e}")

    async def execute_query_async(self, query: str, parameters: Dict = None) -> QueryResult:
        """Thực thi query async với caching"""
        start_time = time.time()
        
        # Check cache first
        cached_result = self.query_cache.get(query, parameters)
        if cached_result is not None:
            self.metrics['cache_hits'] += 1
            return QueryResult(
                data=cached_result,
                execution_time=time.time() - start_time,
                cache_hit=True
            )
        
        # Execute query
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self._execute_query_sync,
                query,
                parameters
            )
            
            # Cache result
            self.query_cache.set(query, result, parameters)
            
            execution_time = time.time() - start_time
            self.metrics['query_count'] += 1
            self.metrics['query_times'].append(execution_time)
            
            return QueryResult(
                data=result,
                execution_time=execution_time,
                cache_hit=False
            )
            
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            return QueryResult(data=[], execution_time=time.time() - start_time)

    def _execute_query_sync(self, query: str, parameters: Dict = None) -> List[Dict]:
        """Thực thi query đồng bộ"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    async def optimized_entity_search(self, entity_name: str, max_depth: int = 3) -> List[Dict]:
        """Tìm kiếm entity với depth limit tối ưu"""
        # Query tối ưu với LIMIT và profile
        optimized_query = f"""
        MATCH path = (source)-[:BAO_GỒM*1..{max_depth}]->(target)
        WHERE source.name CONTAINS $entity_name 
           OR target.name CONTAINS $entity_name
        WITH path, length(path) as depth
        ORDER BY depth
        LIMIT 100
        RETURN path
        """
        
        result = await self.execute_query_async(
            optimized_query, 
            {"entity_name": entity_name}
        )
        
        return result.data

    async def smart_relationship_query(self, source_entity: str, relationship_types: List[str] = None) -> List[Dict]:
        """Query relationships thông minh với filtering"""
        if relationship_types:
            rel_filter = "|".join(relationship_types)
            query = f"""
            MATCH (source)-[r:{rel_filter}]->(target)
            WHERE source.name CONTAINS $source_entity
            RETURN source, r, target, type(r) as rel_type
            ORDER BY rel_type
            LIMIT 50
            """
        else:
            query = """
            MATCH (source)-[r]->(target)
            WHERE source.name CONTAINS $source_entity
            RETURN source, r, target, type(r) as rel_type
            ORDER BY rel_type
            LIMIT 50
            """
        
        result = await self.execute_query_async(
            query,
            {"source_entity": source_entity}
        )
        
        return result.data

    async def parallel_multi_entity_search(self, entities: List[str]) -> Dict[str, List[Dict]]:
        """Tìm kiếm song song nhiều entities"""
        tasks = [
            self.optimized_entity_search(entity)
            for entity in entities
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Tổng hợp kết quả
        entity_results = {}
        for entity, result in zip(entities, results):
            if isinstance(result, Exception):
                self.logger.error(f"Error searching entity {entity}: {result}")
                entity_results[entity] = []
            else:
                entity_results[entity] = result
                
        return entity_results

    async def fuzzy_search_entities(self, search_term: str, similarity_threshold: float = 0.7) -> List[Dict]:
        """Tìm kiếm fuzzy với full-text search"""
        # Sử dụng full-text search index
        query = """
        CALL db.index.fulltext.queryNodes('entity_fulltext', $search_term)
        YIELD node, score
        WHERE score >= $threshold
        RETURN node, score
        ORDER BY score DESC
        LIMIT 20
        """
        
        result = await self.execute_query_async(
            query,
            {
                "search_term": f"{search_term}~",  # Fuzzy search với ~
                "threshold": similarity_threshold
            }
        )
        
        return result.data

    async def get_entity_context(self, entity_name: str, context_radius: int = 2) -> Dict[str, Any]:
        """Lấy context xung quanh entity với radius"""
        # Query lấy context 2 chiều
        context_query = f"""
        MATCH (center)
        WHERE center.name CONTAINS $entity_name
        
        // Lấy neighbors trong radius
        OPTIONAL MATCH path1 = (center)-[*1..{context_radius}]->(outgoing)
        OPTIONAL MATCH path2 = (incoming)-[*1..{context_radius}]->(center)
        
        WITH center, collect(DISTINCT outgoing) as outgoing_nodes, 
             collect(DISTINCT incoming) as incoming_nodes
        
        RETURN center,
               outgoing_nodes,
               incoming_nodes,
               size(outgoing_nodes) as outgoing_count,
               size(incoming_nodes) as incoming_count
        """
        
        result = await self.execute_query_async(
            context_query,
            {"entity_name": entity_name}
        )
        
        return {
            "entity": entity_name,
            "context": result.data,
            "execution_time": result.execution_time
        }

    async def batch_relationship_creation(self, relationships: List[Tuple[Dict, Dict, str]]):
        """Tạo relationships theo batch để tối ưu performance"""
        batch_size = 1000
        total_relationships = len(relationships)
        
        for i in range(0, total_relationships, batch_size):
            batch = relationships[i:i + batch_size]
            await self._create_relationship_batch(batch)
            
            progress = min(i + batch_size, total_relationships)
            self.logger.info(f"Created {progress}/{total_relationships} relationships")

    async def _create_relationship_batch(self, batch: List[Tuple[Dict, Dict, str]]):
        """Tạo một batch relationships"""
        # Tối ưu với UNWIND để bulk operations
        query = """
        UNWIND $batch as rel
        MERGE (source:Entity {name: rel.source.name})
        SET source += rel.source
        MERGE (target:Entity {name: rel.target.name})  
        SET target += rel.target
        MERGE (source)-[r:RELATES_TO {type: rel.relation}]->(target)
        """
        
        batch_data = [
            {
                "source": source,
                "target": target,
                "relation": relation
            }
            for source, target, relation in batch
        ]
        
        await self.execute_query_async(query, {"batch": batch_data})

    def create_triplets_optimized(self, records: List[Dict]) -> List[str]:
        """Tạo triplets tối ưu từ graph records"""
        triplets = []
        
        for record in records:
            try:
                if 'path' in record:
                    path = record['path']
                    
                    # Handle Neo4j Path object
                    if hasattr(path, 'relationships'):
                        relationships = path.relationships
                    elif isinstance(path, dict) and 'relationships' in path:
                        relationships = path['relationships']
                    else:
                        # Try to get relationships from path directly
                        relationships = getattr(path, 'relationships', [])
                    
                    for rel in relationships:
                        try:
                            # Handle Neo4j Relationship object
                            if hasattr(rel, 'start_node') and hasattr(rel, 'end_node'):
                                source_props = dict(rel.start_node) if rel.start_node else {}
                                target_props = dict(rel.end_node) if rel.end_node else {}
                                relation_type = rel.type if hasattr(rel, 'type') else 'UNKNOWN'
                            else:
                                # Fallback for different data structures
                                source_props = {}
                                target_props = {}
                                relation_type = 'UNKNOWN'
                            
                            # Tối ưu format triplet
                            source_name = source_props.get('name', 'Unknown')
                            target_name = target_props.get('name', 'Unknown')
                            
                            triplet = f"{source_name} -> {relation_type} -> {target_name}"
                            triplets.append(triplet)
                            
                        except Exception as e:
                            self.logger.warning(f"Error processing relationship: {e}")
                            continue
                            
            except Exception as e:
                self.logger.warning(f"Error processing record: {e}")
                continue
        
        return list(set(triplets))  # Remove duplicates

    async def intelligent_query_from_question(self, question: str) -> List[str]:
        """Tạo query thông minh từ câu hỏi"""
        # Extract keywords từ question
        keywords = self._extract_keywords_from_question(question)
        
        if not keywords:
            return []
        
        # Tạo query dựa trên keywords
        if len(keywords) == 1:
            # Single entity search
            results = await self.optimized_entity_search(keywords[0])
        else:
            # Multi-entity search
            entity_results = await self.parallel_multi_entity_search(keywords)
            results = []
            for entity_result in entity_results.values():
                results.extend(entity_result)
        
        # Convert thành triplets
        return self.create_triplets_optimized(results)

    def _extract_keywords_from_question(self, question: str) -> List[str]:
        """Extract keywords từ question"""
        # Simple keyword extraction - có thể cải tiến với NLP
        import re
        
        # Remove common words
        common_words = {'là', 'gì', 'nào', 'như', 'thế', 'bao', 'nhiêu', 'khi', 'ở', 'tại', 'của', 'và', 'có'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', question.lower())
        keywords = [word for word in words if len(word) > 2 and word not in common_words]
        
        return keywords[:3]  # Limit to top 3 keywords

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Lấy metrics hiệu năng"""
        cache_total = self.metrics['query_count'] + self.metrics['cache_hits']
        cache_hit_rate = (self.metrics['cache_hits'] / cache_total * 100) if cache_total > 0 else 0
        
        avg_query_time = (
            sum(self.metrics['query_times']) / len(self.metrics['query_times'])
            if self.metrics['query_times'] else 0
        )
        
        return {
            'total_queries': self.metrics['query_count'],
            'cache_hits': self.metrics['cache_hits'],
            'cache_hit_rate': f"{cache_hit_rate:.2f}%",
            'avg_query_time': f"{avg_query_time:.3f}s",
            'cache_size': len(self.query_cache.cache),
            'connection_pool_size': self.driver.get_pool_status()
        }

    async def health_check(self) -> bool:
        """Kiểm tra health của database"""
        try:
            result = await self.execute_query_async("RETURN 1 as health_check")
            return len(result.data) > 0
        except:
            return False

    def close(self):
        """Đóng connections"""
        self.driver.close()
        self.executor.shutdown(wait=True)
