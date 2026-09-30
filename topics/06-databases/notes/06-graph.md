# 06 — Graph DBs: Family Trees That Answer Questions (Neo4j/Cypher → knowledge graphs)

## 1. Property graph (nodes + labeled arrows, both carry luggage)

```
(:User {name:"Asha"})-[:BOUGHT {at:"2026-01-02"}]->(:Item {name:"DosaMix"})
(:User)-[:FRIEND]->(:User)      // fraud rings, recommendations = path patterns!
```

- **Cypher** reads like ASCII art: `MATCH (u:User)-[:BOUGHT]->(i:Item) WHERE u.city='Blr' RETURN i.name, count(*) ORDER BY 2 DESC`.
- vs SQL: 5-hop friend-of-friend in SQL = 5 self-joins (planner weeps); in graph = pointer hops (fast!). vs documents: graphs JOIN cheaply, documents embed cheaply.

## 2. RDF/SPARQL (the librarian's formal cousin)

Triples `(subject, predicate, object)` + ontologies (OWL: "every Refund needs an Order"). **SPARQL** queries the triple store (Wikidata runs on this!). Use when: open data, reasoning/inference ("all mammals…"), standards matter more than speed.

## 3. Where graphs win (interview examples!)

- **Fraud**: shared phone/device/IP across "strangers" → ring pattern `(a)-[:USES]->(device)<-[:USES]-(b)` + velocity.
- **Recommendations**: collaborative `(you)-[:BOUGHT]->(x)<-[:BOUGHT]-(stranger)-[:BOUGHT]->(y)` = "bought x, also bought y".
- **Knowledge graphs + LLM** (topic 19 GraphRAG!): entities/relations as retrievable context with provenance (citations per hop!).
- Access control (ReBAC: "edit if writer of parent folder"), dependency blast-radius, org charts.

Engines: **Neo4j/Cypher** (default answer), Memgraph (fast, same language), Neptune (managed, Gremlin+SPARQL), ArangoDB (multi-model), **Gremlin** (traversal language across vendors).

Runnable BFS recommendation + fraud-ring finder (adjacency maps, same traversals): `../examples/08_graph_traversal.js`.
