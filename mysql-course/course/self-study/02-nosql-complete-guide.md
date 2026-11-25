# Self-Study 2 — High-ROI NoSQL & Polyglot Persistence Guide (Slides 39–105)

> **For Candidates & AI Agents:** Study this **after** Module 4. It covers the essential NoSQL concepts, data-modeling rules, and query patterns from slides 39–105 that candidates actually need for engineering work and interviews — without overwhelming you with low-value cloud/script trivia.

---

### N1 — CAP Theorem, BASE vs ACID & The Golden NoSQL Rule
- **Story Anchor:** *Sticky Notes vs Filing Cabinets* — SQL puts strict structure inside the database (ACID); NoSQL gives you speed, horizontal scale, or specialized shapes (JSON, RAM key-value, graphs, text search, vectors), **moving schema validation into your application code**.
- **CAP Theorem (for distributed databases):** When a network **P**artition splits nodes, you must choose **C**onsistency (reject or wait rather than return stale data) or **A**vailability (respond even if a node hasn't synced yet).
- **BASE vs ACID:** Relational DBs prioritize **ACID** (immediate consistency). Many distributed NoSQL systems prioritize **BASE** (Basically Available, Soft state, **Eventual Consistency** — replicas catch up within milliseconds).
- **Check Q:** During a network partition between two database replicas, what trade-off does CAP force? — **A:** Consistency (every read sees the latest write, or errors) vs Availability (every request gets a non-error response, possibly stale).

---

### N2 — MongoDB (Document Database — Slides 41–57)
- **What it is:** Stores JSON-like **BSON** (Binary JSON) documents inside **Collections** (analogous to rows inside tables), with flexible schemas.
- **The #1 Interview Question — Embedding vs Referencing:**
  - **Embed** sub-documents/arrays *inside* one document when data is read together and bounded (`{ name: "Alice", skills: ["SQL", "Python"] }`) -> fast single-read, atomic per-document update!
  - **Reference** by ID across collections when data grows unboundedly (millions of activity logs) or is shared/updated independently (`course_id` in enrollments).
- **Essential MongoDB CRUD & Aggregation Syntax:**
  ```javascript
  // CRUD
  db.students.insertOne({ name: "Alice", age: 22, skills: ["SQL", "Python"] });
  db.students.find({ name: "Alice" });
  db.students.updateOne({ name: "Alice" }, { $set: { age: 23 } });
  db.students.deleteOne({ name: "Alice" });

  // Index & Aggregation Pipeline
  db.students.createIndex({ name: 1 });
  db.students.aggregate([
    { $match: { age: { $gte: 20 } } },
    { $group: { _id: "$course", avgAge: { $avg: "$age" } } }
  ]);
  ```
- **Scaling & HA:** **Replica Sets** (primary + secondaries for automatic failover) and **Sharding** (distributing documents across servers by a shard key). Supports multi-document ACID transactions when needed, though single-document atomicity is the sweet spot.
- **Check Q:** Why is embedding 100,000 log events inside a single `student` document a bad MongoDB design? — **A:** Unbounded growth hits MongoDB's 16 MB document size limit and degrades read/write performance — use referencing instead.

---

### N3 — Redis (In-Memory Key-Value Store — Slides 58–71, Runnable in Docker!)
- **What it is:** An open-source, in-memory data structure store used as a **cache, session store, rate limiter, leaderboard, and message broker**.
- **Essential Data Structures & Use Cases:**
  | Type | Example Command | Real Use Case |
  |---|---|---|
  | **String** | `SET rate:user:1 5 EX 60` / `INCR rate:user:1` | Counters, rate limiters, cached JSON |
  | **Hash** | `HSET student:101 name "Alice" grade "A"` / `HGETALL student:101` | Storing compact user/course objects |
  | **Set** | `SADD student:101:courses "1" "3"` / `SMEMBERS student:101:courses` | Unique memberships, tags |
  | **Sorted Set** | `ZADD leaderboard 95 "Alice" 88 "Bob"` / `ZREVRANGE leaderboard 0 2 WITHSCORES` | Top-N leaderboards, sliding-window rate limits |
- **Persistence (Classic Interview Question — Slide 68):**
  - **RDB (Snapshots):** periodic point-in-time dumps (fast restarts, small files, can lose last few seconds/minutes on crash).
  - **AOF (Append-Only File):** logs every write command (minimal data loss, larger file). Production Redis often pairs RDB + AOF!
- **Atomic Grouping & Expiry:** `MULTI ... EXEC` queues commands atomically; `EXPIRE key 3600` / `TTL key` bounds cache staleness.
- **Try it live on our container:**
  ```bash
  docker compose exec -T redis redis-cli HSET student:101 name "Alice" age "22"
  docker compose exec -T redis redis-cli HGETALL student:101
  docker compose exec -T redis redis-cli EXPIRE student:101 60
  docker compose exec -T redis redis-cli DEL student:101
  ```
- **Check Q:** What is the trade-off between Redis RDB snapshots and AOF logs? — **A:** RDB is compact and restarts fast but risks losing writes since the last snapshot; AOF logs every write for higher durability at slightly higher disk/IO cost.

---

### N4 — Elasticsearch (Search & Analytics Engine — Slides 88–103)
- **What it is:** Distributed RESTful search/analytics engine built on **Apache Lucene** (part of the ELK stack).
- **Why MySQL `LIKE '%machine%'` fails where Elasticsearch shines:** A leading `%` wildcard disables MySQL B-Tree indexes (forcing a full scan) and cannot rank relevance or tolerate typos. Elasticsearch builds an **Inverted Index** (word -> list of document IDs) via **Analyzers** (tokenizing, lowercasing, stemming).
- **Core Concepts:** Cluster -> Node -> Index (collection of JSON docs) -> **Shards** (parallelism/scale) + **Replicas** (HA/read throughput) + **Mapping** (field types).
- **Key Query Distinction (`match` vs `term`):**
  - `match`: analyzes the search string (e.g., `"Machine Learning"` finds `"machine learning"` with relevance scoring).
  - `term`: exact unanalyzed match (for booleans, IDs, status tags like `is_online: true`).
  - `range`: numeric/date filtering (`price_usd < 500`).
- **Golden Rule:** Elasticsearch is **never your primary source of truth** (keep authoritative records in MySQL and sync/index into Elasticsearch).
- **Check Q:** When querying Elasticsearch for an exact status flag or keyword ID, should you use `match` or `term`? — **A:** `term` (exact, unanalyzed match); `match` is for analyzed full-text search.

---

### N5 — VectorDB & Neo4j (AI Search & Graph Relationships — Slides 72–87, 104–105)
- **Vector Databases (VectorDB — Slides 104–105):**
  - Stores high-dimensional **embeddings** (numerical arrays from ML models capturing semantic meaning of text, images, or audio).
  - Finds conceptually similar content via **Cosine Similarity** / nearest neighbors (e.g., searching `"warm jacket for wet winters"` matches `"waterproof winter parka"` even with zero overlapping words).
  - **Production RAG rule:** Combine Vector Similarity + **Metadata Filters** (tenant, permissions, date) + Keyword (**Hybrid Search**) so exact product IDs/acronyms aren't missed!
- **Neo4j (Graph Database — Slides 72–87):**
  - Stores **Nodes** (entities with Labels + Properties) and **Relationships** (typed, directed edges with Properties), queried via **Cypher** (`MATCH (s:Student)-[:ENROLLED_IN]->(c:Course) RETURN s, c;`).
  - **When to pick Neo4j over MySQL:** When queries traverse **3+ hops of connected relationships** (social friend-of-friend graphs, fraud rings, `shortestPath`), where SQL recursive CTEs or repeated self-joins become slow and complex.
- **Check Q:** Why does a production RAG system pair Vector similarity search with Metadata Filters? — **A:** Semantic similarity alone ignores hard access/business constraints like tenant ID, document permissions, or effective date.

---

## Self-Study Quiz Bank (For AI Quiz Mode)
1. Explain CAP theorem in one concrete distributed-database scenario.
2. In MongoDB, when should you embed a sub-document vs reference another collection?
3. Which Redis data structure fits a real-time top-10 student leaderboard, and why?
4. Contrast Redis RDB vs AOF persistence.
5. Why does Elasticsearch beat MySQL `LIKE '%keyword%'` on 10 million course descriptions?
6. In Elasticsearch, when do you use `match` vs `term`?
7. When does Neo4j outperform MySQL on relationship queries?
8. What does a VectorDB store, and why do production RAG apps combine vector search with metadata filters?
