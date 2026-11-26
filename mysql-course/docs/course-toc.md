# MySQL & NoSQL Essentials — 2-Hour Class Table of Contents

Designed for a **2-hour (120-minute) live instructor session** + **structured AI-guided candidate self-study** (`training_db` in Docker Compose).
Low-ROI / redundant topics (ISAM/network history trivia, `VARCHAR2` Oracle tangents, `NATURAL JOIN` drills, writing complex legacy stored procedures live) are intentionally trimmed so every minute covers high-signal production engineering skills.

| # | Module | 2-Hr Budget | Topics Covered (High-Impact Only) | Lab File |
|---|---|---|---|---|
| **1** | Foundations, Setup, Types, Constraints & 3NF | **25 min** (`0:00–0:25`) | RDBMS vs flat files, SQL vs NoSQL ("moves schema to code"), TCP:3306, `INT`/`VARCHAR`/`TEXT`/`DATE`/`DECIMAL`, 5 Constraints, 1NF/2NF/3NF | [01-foundations-schema-normalization.md](../course/modules/01-foundations-schema-normalization.md) |
| **2** | Queries, Joins, `GROUP BY`/`HAVING`, CTEs & Window Functions | **35 min** (`0:25–1:00`) | Safe CRUD, `IS NULL` vs `= NULL`, `WHERE` vs `HAVING`, `INNER JOIN` duplicated-rows bug, `LEFT JOIN` anti-join, `NOT EXISTS` vs `NOT IN` NULL trap, `WITH` / `WITH RECURSIVE`, Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `SUM OVER`) | [02-queries-joins-ctes-windows.md](../course/modules/02-queries-joins-ctes-windows.md) |
| **3** | Transactions, Locking, Indexing & `EXPLAIN ANALYZE` | **30 min** (`1:00–1:30`) | ACID & DDL implicit commit, `REPEATABLE READ` + MVCC, `SELECT ... FOR UPDATE` vs optimistic locking, deadlocks, `enrollment_log` trigger + Stored Proc vs App-code rule, Composite/Covering Indexes (Leftmost Prefix, SARGability), `EXPLAIN ANALYZE` + Keyset vs `OFFSET` pagination + N+1 | [03-transactions-locking-indexing-explain.md](../course/modules/03-transactions-locking-indexing-explain.md) |
| **4** | Caching, Scaling (Partitioning/Sharding), NoSQL & Live Fault Check | **30 min** (`1:30–2:00`) | Redis Cache-Aside (TTL + invalidation), 5-step Scaling Ladder (Read Replicas, `PARTITION BY RANGE`, Sharding trade-offs), CAP & 5 NoSQL families (MongoDB, Redis, Neo4j, Elasticsearch, VectorDB), 2 live `scripts/break.sh` faults | [04-caching-scaling-nosql-practice.md](../course/modules/04-caching-scaling-nosql-practice.md) |

## Post-Class Candidate Self-Study (Outside the 2-Hour Clock)
| # | Pack | Target Timing | High-ROI Topics Covered | File |
|---|---|---|---|---|
| **S1** | Senior SQL Deep Dive | After Modules 1–4 | `CASE WHEN`/`COALESCE`, `SELF JOIN`/`FULL JOIN` emulation/`INTERSECT`/`EXCEPT`, `LEAD`/Window frames, `VIEW` vs CTE vs Temp Table, Gap locks, SQL Injection, Procedures/Functions syntax, `mysqldump` & Zero-Downtime Migrations | [01-sql-senior-deep-dive.md](../course/self-study/01-sql-senior-deep-dive.md) |
| **S2** | High-ROI NoSQL Guide | After Module 4 | CAP & BASE vs ACID, MongoDB (Embed vs Reference, CRUD, `$group`), Redis (Strings/Hashes/Sets/Sorted Sets, RDB vs AOF), Elasticsearch (`match` vs `term`), VectorDB (RAG + metadata filters), Neo4j Cypher | [02-nosql-complete-guide.md](../course/self-study/02-nosql-complete-guide.md) |

## Slide Clarifications (Embedded in Beats)
- **Slide 16–17:** MySQL uses `VARCHAR` (variable-length), not Oracle `VARCHAR2`; `CHAR` is fixed-length.
- **Slide 24:** MySQL 8.0 has no `FULL OUTER JOIN` keyword (use `LEFT JOIN ... UNION ... RIGHT JOIN` if ever needed).
- **Slide 35:** `01-schema.sql` pairs `enrollment_log` with `trg_after_enrollment_insert`.
- **Slide 38:** MySQL 8.0 removed the built-in query cache; use Redis cache-aside (`:6379`).
