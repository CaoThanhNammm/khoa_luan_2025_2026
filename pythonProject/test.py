relationship = {'extracted': {'entities': {'entity': 'website', 'type': 'website'}, 'relations': {'source': 'khoa thủy sản', 'target': 'website', 'relation': 'có'}}, 'retriever': 'graph'}
relationship = relationship['extracted']['relations']

question = " ".join(f"{r['source']} {r['relation']} {r['target']}" for r in relationship)
print(question)