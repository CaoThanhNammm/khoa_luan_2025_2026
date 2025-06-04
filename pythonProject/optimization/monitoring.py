"""
Monitoring và Metrics Dashboard
"""

import asyncio
import time
import psutil
import GPUtil
from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass, asdict
from threading import Thread
import queue
import sqlite3
import pandas as pd

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    gpu_utilization: float
    gpu_memory_used: float
    disk_io_read: float
    disk_io_write: float
    network_bytes_sent: float
    network_bytes_recv: float

@dataclass
class ApplicationMetrics:
    """Application-specific metrics"""
    timestamp: float
    total_queries: int
    avg_response_time: float
    cache_hit_rate: float
    active_connections: int
    errors_count: int
    qdrant_queries: int
    neo4j_queries: int
    embedding_generations: int

class MetricsCollector:
    """Collect system và application metrics"""
    
    def __init__(self, collection_interval: int = 5):
        self.collection_interval = collection_interval
        self.running = False
        self.metrics_queue = queue.Queue()
        self.db_path = "optimization/metrics.db"
        self._init_database()
        
        # Application components (to be injected)
        self.optimized_chat = None
        
        self.logger = logging.getLogger(__name__)
    
    def _init_database(self):
        """Initialize SQLite database for metrics storage"""
        conn = sqlite3.connect(self.db_path)
        
        # System metrics table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                timestamp REAL PRIMARY KEY,
                cpu_percent REAL,
                memory_percent REAL,
                memory_used_gb REAL,
                gpu_utilization REAL,
                gpu_memory_used REAL,
                disk_io_read REAL,
                disk_io_write REAL,
                network_bytes_sent REAL,
                network_bytes_recv REAL
            )
        ''')
        
        # Application metrics table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS app_metrics (
                timestamp REAL PRIMARY KEY,
                total_queries INTEGER,
                avg_response_time REAL,
                cache_hit_rate REAL,
                active_connections INTEGER,
                errors_count INTEGER,
                qdrant_queries INTEGER,
                neo4j_queries INTEGER,
                embedding_generations INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # GPU metrics (if available)
            gpu_utilization = 0
            gpu_memory_used = 0
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_utilization = gpu.load * 100
                    gpu_memory_used = gpu.memoryUsed
            except:
                pass
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            
            # Network
            network_io = psutil.net_io_counters()
            
            return SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_gb=memory.used / (1024**3),
                gpu_utilization=gpu_utilization,
                gpu_memory_used=gpu_memory_used,
                disk_io_read=disk_io.read_bytes if disk_io else 0,
                disk_io_write=disk_io.write_bytes if disk_io else 0,
                network_bytes_sent=network_io.bytes_sent if network_io else 0,
                network_bytes_recv=network_io.bytes_recv if network_io else 0
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
            return None
    
    def collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-specific metrics"""
        try:
            if not self.optimized_chat:
                return None
            
            # Get metrics from optimized chat
            chat_metrics = self.optimized_chat.get_performance_metrics()
            
            # Extract relevant metrics
            total_queries = chat_metrics['chat_metrics']['total_queries']
            
            # Parse average response time (remove 's' suffix)
            avg_time_str = chat_metrics['chat_metrics']['avg_response_time']
            avg_response_time = float(avg_time_str.replace('s', ''))
            
            # Parse cache hit rate (remove '%' suffix)
            cache_rate_str = chat_metrics['chat_metrics']['cache_hit_rate']
            cache_hit_rate = float(cache_rate_str.replace('%', ''))
            
            # Get component metrics
            qdrant_metrics = chat_metrics.get('qdrant_metrics', {})
            neo4j_metrics = chat_metrics.get('neo4j_metrics', {})
            
            return ApplicationMetrics(
                timestamp=time.time(),
                total_queries=total_queries,
                avg_response_time=avg_response_time,
                cache_hit_rate=cache_hit_rate,
                active_connections=0,  # Can be enhanced
                errors_count=0,  # Can be enhanced
                qdrant_queries=qdrant_metrics.get('total_queries', 0),
                neo4j_queries=neo4j_metrics.get('total_queries', 0),
                embedding_generations=0  # Can be enhanced
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting application metrics: {e}")
            return None
    
    def store_metrics(self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics):
        """Store metrics in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            if system_metrics:
                conn.execute('''
                    INSERT OR REPLACE INTO system_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    system_metrics.timestamp,
                    system_metrics.cpu_percent,
                    system_metrics.memory_percent,
                    system_metrics.memory_used_gb,
                    system_metrics.gpu_utilization,
                    system_metrics.gpu_memory_used,
                    system_metrics.disk_io_read,
                    system_metrics.disk_io_write,
                    system_metrics.network_bytes_sent,
                    system_metrics.network_bytes_recv
                ))
            
            if app_metrics:
                conn.execute('''
                    INSERT OR REPLACE INTO app_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    app_metrics.timestamp,
                    app_metrics.total_queries,
                    app_metrics.avg_response_time,
                    app_metrics.cache_hit_rate,
                    app_metrics.active_connections,
                    app_metrics.errors_count,
                    app_metrics.qdrant_queries,
                    app_metrics.neo4j_queries,
                    app_metrics.embedding_generations
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error storing metrics: {e}")
    
    def start_collection(self):
        """Start metrics collection in background thread"""
        self.running = True
        collection_thread = Thread(target=self._collection_loop)
        collection_thread.daemon = True
        collection_thread.start()
        
        self.logger.info("Metrics collection started")
    
    def stop_collection(self):
        """Stop metrics collection"""
        self.running = False
        self.logger.info("Metrics collection stopped")
    
    def _collection_loop(self):
        """Main collection loop"""
        while self.running:
            try:
                # Collect metrics
                system_metrics = self.collect_system_metrics()
                app_metrics = self.collect_application_metrics()
                
                # Store metrics
                self.store_metrics(system_metrics, app_metrics)
                
                # Sleep until next collection
                time.sleep(self.collection_interval)
                
            except Exception as e:
                self.logger.error(f"Error in collection loop: {e}")
                time.sleep(self.collection_interval)
    
    def get_recent_metrics(self, hours: int = 1) -> Dict[str, Any]:
        """Get recent metrics for dashboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Calculate time threshold
            threshold = time.time() - (hours * 3600)
            
            # Get system metrics
            system_df = pd.read_sql_query(
                "SELECT * FROM system_metrics WHERE timestamp > ? ORDER BY timestamp",
                conn, params=[threshold]
            )
            
            # Get application metrics
            app_df = pd.read_sql_query(
                "SELECT * FROM app_metrics WHERE timestamp > ? ORDER BY timestamp",
                conn, params=[threshold]
            )
            
            conn.close()
            
            return {
                'system_metrics': system_df.to_dict('records'),
                'application_metrics': app_df.to_dict('records'),
                'summary': {
                    'avg_cpu': system_df['cpu_percent'].mean() if not system_df.empty else 0,
                    'avg_memory': system_df['memory_percent'].mean() if not system_df.empty else 0,
                    'avg_response_time': app_df['avg_response_time'].mean() if not app_df.empty else 0,
                    'current_cache_hit_rate': app_df['cache_hit_rate'].iloc[-1] if not app_df.empty else 0,
                    'total_queries': app_df['total_queries'].max() if not app_df.empty else 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting recent metrics: {e}")
            return {}

class AlertManager:
    """Manage performance alerts"""
    
    def __init__(self):
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'avg_response_time': 5.0,
            'cache_hit_rate': 30.0,  # Minimum acceptable rate
            'gpu_utilization': 90.0
        }
        
        self.alerts_history = []
        self.logger = logging.getLogger(__name__)
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for performance alerts"""
        alerts = []
        
        try:
            # Get latest metrics
            if 'system_metrics' in metrics and metrics['system_metrics']:
                latest_system = metrics['system_metrics'][-1]
                
                # CPU alert
                if latest_system['cpu_percent'] > self.thresholds['cpu_percent']:
                    alerts.append({
                        'type': 'cpu_high',
                        'message': f"High CPU usage: {latest_system['cpu_percent']:.1f}%",
                        'severity': 'warning',
                        'timestamp': latest_system['timestamp']
                    })
                
                # Memory alert
                if latest_system['memory_percent'] > self.thresholds['memory_percent']:
                    alerts.append({
                        'type': 'memory_high',
                        'message': f"High memory usage: {latest_system['memory_percent']:.1f}%",
                        'severity': 'warning',
                        'timestamp': latest_system['timestamp']
                    })
                
                # GPU alert
                if latest_system['gpu_utilization'] > self.thresholds['gpu_utilization']:
                    alerts.append({
                        'type': 'gpu_high',
                        'message': f"High GPU usage: {latest_system['gpu_utilization']:.1f}%",
                        'severity': 'warning',
                        'timestamp': latest_system['timestamp']
                    })
            
            if 'application_metrics' in metrics and metrics['application_metrics']:
                latest_app = metrics['application_metrics'][-1]
                
                # Response time alert
                if latest_app['avg_response_time'] > self.thresholds['avg_response_time']:
                    alerts.append({
                        'type': 'response_time_high',
                        'message': f"High response time: {latest_app['avg_response_time']:.2f}s",
                        'severity': 'critical',
                        'timestamp': latest_app['timestamp']
                    })
                
                # Cache hit rate alert
                if latest_app['cache_hit_rate'] < self.thresholds['cache_hit_rate']:
                    alerts.append({
                        'type': 'cache_rate_low',
                        'message': f"Low cache hit rate: {latest_app['cache_hit_rate']:.1f}%",
                        'severity': 'warning',
                        'timestamp': latest_app['timestamp']
                    })
            
            # Store alerts
            for alert in alerts:
                self.alerts_history.append(alert)
                self.logger.warning(f"ALERT: {alert['message']}")
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
            return []
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        threshold = time.time() - (hours * 3600)
        return [
            alert for alert in self.alerts_history 
            if alert['timestamp'] > threshold
        ]

# Global metrics collector instance
metrics_collector = MetricsCollector()
alert_manager = AlertManager()

def start_monitoring(optimized_chat=None):
    """Start monitoring system"""
    global metrics_collector
    
    if optimized_chat:
        metrics_collector.optimized_chat = optimized_chat
    
    metrics_collector.start_collection()

def stop_monitoring():
    """Stop monitoring system"""
    global metrics_collector
    metrics_collector.stop_collection()

def get_dashboard_data(hours: int = 1) -> Dict[str, Any]:
    """Get data for monitoring dashboard"""
    global metrics_collector, alert_manager
    
    # Get recent metrics
    metrics = metrics_collector.get_recent_metrics(hours)
    
    # Check for alerts
    alerts = alert_manager.check_alerts(metrics)
    
    # Add alerts to response
    metrics['alerts'] = alerts
    metrics['recent_alerts'] = alert_manager.get_recent_alerts(hours=24)
    
    return metrics
