# Module 4 — Caching, Scaling (Partitioning/Sharding), NoSQL & Live Fault Check (30 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **30 minutes** (`1:30–2:00`).
Deck slides: 5, 38–40 (plus rapid architectural synthesis of 41–105: MongoDB, Redis, Neo4j, Elasticsearch, VectorDB).
Story anchor: **The Highway & The Tool Belt** — when one MySQL road jams, don't immediately tear up the highway (Sharding). First tune queries, add a corner shop (**Redis Cache**), add read lanes (**Read Replicas**), split old logs into removable containers (**Partitioning**), and pick the right **NoSQL** specialist when a relational table isn't the right shape.
Stack requirements: `scripts/setup.sh` READY (MySQL + Redis), `scripts/fix.sh` clean baseline.

## Objectives
Implement Redis cache-aside with invalidation, walk the 5-step MySQL scaling ladder (Partitioning vs Sharding trade-offs), choose accurately across MySQL and 5 NoSQL families using CAP/ACID criteria, and diagnose live DB faults from SQL/EXPLAIN/Redis evidence.

---

### Beat 4.1 — Caching (Redis Cache-Aside) & The 5-Step Scaling Ladder (10 min)
- **Slides:** 8, 38 + Senior Scaling Architecture
- **Say:**
  - **MySQL 8.0 removed its legacy Query Cache** (global write lock bottleneck). Modern apps use **Redis Cache-Aside**: check Redis -> on Miss, query MySQL, `SET` in Redis with `TTL` -> on write, `DEL` key to avoid **stale data**.
  - **The Scaling Ladder (in order!):**
    1. Indexes & query fixes (`EXPLAIN ANALYZE`)
    2. Redis cache for hot reads
    3. **Read Replicas** (offload reads via binlog; trade-off = **replication lag**)
    4. **Table Partitioning (`PARTITION BY RANGE`)** on one server — best for time-series logs (`DROP PARTITION` deletes millions of old rows instantly)
    5. **Horizontal Sharding** across servers by a Shard Key — **last resort** (breaks cross-shard `JOIN`s, complicates transactions & global IDs).
- **Demo (run: agent):** Redis Cache-Aside + quick `PARTITION BY RANGE` inspection.
  ```bash
  docker compose exec -T redis redis-cli SET "course:1" '{"id":1,"name":"Data Science","price":499.00}' EX 60
  docker compose exec -T redis redis-cli GET "course:1"
  docker compose exec -T redis redis-cli DEL "course:1"
  scripts/sql.sh "CREATE TABLE _part_demo (id INT NOT NULL, yr INT NOT NULL, PRIMARY KEY (id, yr)) PARTITION BY RANGE (yr) (PARTITION p2024 VALUES LESS THAN (2025), PARTITION p2025 VALUES LESS THAN (2026)); SELECT PARTITION_NAME FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME='_part_demo'; DROP TABLE _part_demo;"
  ```
  **Point out:** Partitioning splits storage inside *one* MySQL node (PK must include partition key); Sharding splits across *multiple* nodes.
- **Candidate takeaway:** *"Climb the scaling ladder in order — never shard for read load when indexes, Redis, and read replicas solve it cleanly."*
- **Ask:**
  - Q: Read traffic is 10x write traffic and MySQL CPU is high. Shard first or Read Replicas + Redis? — A: Redis + Read Replicas; Sharding is a last resort for write/storage ceilings.
  - Q: Why is `PARTITION BY RANGE (year)` great for large log tables? — A: Partition pruning on date queries plus instant old-data purge with `DROP PARTITION`.
- **Done when:** candidates distinguish Partitioning vs Sharding vs Read Replicas.

### Beat 4.2 — NoSQL Essentials & Polyglot Persistence (10 min)
- **Slides:** 5, 39–40 (synthesizing MongoDB 41–57, Redis 58–71, Neo4j 72–87, Elasticsearch 88–103, VectorDB 104–105)
- **Say:**
  - **CAP Theorem:** Under a network **P**artition, distributed stores trade **C**onsistency vs **A**vailability (SQL = ACID; many NoSQL = BASE / eventual consistency).
  - **The 5 NoSQL Tools & When Each Beats MySQL:**
    1. **Document (MongoDB):** flexible JSON/BSON documents, nested forms/catalogs, horizontal sharding. *(Avoid for multi-table financial invariants.)*
    2. **In-Memory Key-Value (Redis):** sub-ms cache, sessions, rate limits, leaderboards (`TTL`, `INCR`, sorted sets).
    3. **Graph (Neo4j):** nodes + edges (Cypher) — fraud rings, social graphs, 4+ hop traversals where SQL joins crawl.
    4. **Search Engine (Elasticsearch):** Lucene inverted index for typo-tolerant full-text search & log analytics — *not* primary source of truth.
    5. **Vector DB:** stores ML embeddings for semantic similarity (cosine distance) in AI/RAG apps.
  - **Polyglot Persistence:** real systems combine MySQL (enrollments, payments) + Redis (cache/sessions) + Elasticsearch (course search) + VectorDB (AI tutor).
- **Candidate takeaway:** *"Pick the DB by access pattern: MySQL for relational ACID truth, Redis for speed/TTL, MongoDB for evolving documents, Neo4j for multi-hop graphs, Elasticsearch for full-text, VectorDB for semantic AI."*
- **Ask:**
  - Q: For a Training Platform, pick the right DB for: (a) billing & enrollments, (b) typo-tolerant course search, (c) semantic Q&A over PDFs, (d) API rate limiting. — A: (a) MySQL, (b) Elasticsearch, (c) VectorDB, (d) Redis.
- **Done when:** candidates match all 5 NoSQL families to real engineering tasks.

### Beat 4.3 — Live 10-Minute Fault Diagnosis (`scripts/break.sh`) (10 min)
- **Slides:** none (live terminal close)
- **Say:** Close the 2-hour class by diagnosing 2 live faults from evidence alone, then hand over the post-class Capstone Lab.
- **Demo (run: agent):** inject 2 faults (or 3 if time permits), let candidates diagnose from the symptom, then `scripts/fix.sh`.
  ```bash
  scripts/break.sh duplicate-join
  scripts/sql.sh "SELECT * FROM v_course_revenue_report;"
  # Ask room: Why is Data Science revenue wildly inflated? -> SHOW CREATE VIEW v_course_revenue_report\G

  scripts/break.sh stale-cache
  docker compose exec -T redis redis-cli GET "courses:active"
  scripts/sql.sh "SELECT id, name, price FROM course;"
  # Ask room: Why do Redis and MySQL disagree? -> TTL + missing invalidation

  scripts/fix.sh
  ```
  **Point out:** Other faults (`missing-index`, `broken-trigger`, `null-trap`, `orphan-fk`) are ready in `scripts/break.sh` for candidates' post-class practice!
- **Candidate takeaway:** *"Diagnose from evidence first (`SHOW CREATE VIEW`, `EXPLAIN ANALYZE`, `SHOW TRIGGERS`, `redis-cli TTL`) before touching production data."*
- **Ask:**
  - Q: A cached course price in Redis disagrees with MySQL. Immediate fix + long-term fix? — A: Immediate: `DEL` the Redis key; Long-term: invalidate/update cache on every MySQL write + keep a bounded TTL.
- **Done when:** candidates diagnose both live faults from evidence.

---

## Post-Class Practice & Capstone (Candidates)
1. Complete `db/labs/module-04-scaling-nosql-capstone.sql` (design 3NF `assignment` + `submission` tables, `JOIN` + `GROUP BY` + `HAVING`, anti-join, `DENSE_RANK()` window function, and practice `scripts/break.sh`).
2. Run an 8-question Quiz with ChatGPT / `practice-mysql` and send your **Daily Report** to the instructor.
