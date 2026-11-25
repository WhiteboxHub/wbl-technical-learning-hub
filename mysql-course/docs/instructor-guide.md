# Instructor Guide — 2-Hour MySQL & NoSQL Class

Teach MySQL, Concurrency, Query Performance & NoSQL Essentials cleanly inside a **2-hour (120-minute)** live session using an AI co-pilot and the shared **Training Management DB** (`training_db`).

**In a hurry? See the [Class-Day Quick Start](class-day-quickstart.md).**

---

## 1. How the 2-Hour Class Works
- **You teach; the agent keeps the 120-minute clock.** It runs live SQL/Redis demos via `scripts/sql.sh`, displays plain-English **Candidate Takeaways** so students can explain every concept back, and holds quiz answers until you ask.
- **Why only 4 Modules?** Low-ROI topics (pre-DB ISAM/network history, Oracle `VARCHAR2` tangents, `NATURAL`/`RIGHT JOIN` drills, writing complex stored procedures live) were cut so you finish every high-value topic in **120 minutes** without rushing.
- **The Storytelling Rule:** *Tell them what you are going to tell them -> Tell them -> Tell them what you told them* using each module's Story Anchor.

| # | Module | 2-Hr Budget | Story Anchor |
|---|---|---|---|
| 1 | Foundations, Setup, Types, Constraints & 3NF | **25 min** | The Labelled Filing Room |
| 2 | Queries, Joins, `GROUP BY`/`HAVING`, CTEs & Window Functions | **35 min** | The Wedding Guest Lists & The Ranked Ledger |
| 3 | Transactions, Locking, Indexing & `EXPLAIN ANALYZE` | **30 min** | The Vault Clerk & The Index Tab |
| 4 | Caching, Scaling (Partitioning/Sharding), NoSQL & Live Fault Check | **30 min** | The Highway & The Tool Belt |

---

## 2. Before Class (One Time)
1. Install **Docker Desktop** and an AI coding agent (**Claude Code**, **Antigravity**, or **Cursor**).
2. Open `wbl-technical-learning-hub/mysql-course` in a **new session**.
3. Say **"set up the class"** (`setup-mysql-class`). Wait for **READY** (`:3306`, `:8082`, `:6379`).
4. Say **"teach class"** (or **"teach module 1"** … **"teach module 4"**).

**If running behind during class:** skip the second `Ask` question in Beats 1.2, 2.1, or 3.2. Never skip **Beat 2.2 (Joins/NULL trap)**, **Beat 2.3 (CTEs/Window Functions)**, **Beat 3.3 (Composite Index/`EXPLAIN ANALYZE`)**, or **Beat 4.2 (NoSQL decision matrix)**.

---

## 3. Known Facts About `training_db`
- **8 students**, **6 courses**, **12 enrollments** (Students 7 & 8 have 0 enrollments; Course 6 has 0 enrollments; Students 3 & 6 have `phone IS NULL`; Students 1 & 6 have `mentor_id IS NULL`).
- `trg_after_enrollment_insert` is active from startup -> `enrollment_log` starts with 12 rows.
- `activity_log` has **2,000 rows** so `EXPLAIN ANALYZE` clearly contrasts `type: ALL` vs composite index `range` + `Using index` and `OFFSET` vs Keyset pagination.
- `scripts/break.sh <fault>` supports `duplicate-join`, `missing-index`, `broken-trigger`, `null-trap`, `orphan-fk`, `stale-cache`; `scripts/fix.sh` restores the clean baseline.

---

## 4. Candidate Self-Study Loop (After the 2-Hour Class)
Send candidates [docs/student-guide.md](student-guide.md) and [prompts/chatgpt-quick-prompts.md](../prompts/chatgpt-quick-prompts.md). They paste the repo into **ChatGPT, Claude, Antigravity, or any coding agent** to:
1. Re-learn any Beat from `course/modules/01–04` with its Story Anchor and practice **explaining the Candidate Takeaway in their own words**
2. Complete the 4 hands-on labs in `db/labs/` (predicting row counts before running) and debug SQL with the **4-Rung Hint Ladder**
3. Continue into `course/self-study/01–02` for deeper senior SQL & NoSQL topics not covered in the 2-hour clock (`CASE WHEN`, Gap locks, SQL Injection, Zero-Downtime Migrations, MongoDB, Redis, Elasticsearch, VectorDB, Neo4j)
4. Take an 8-question end-of-module quiz and send you their **Daily Report**.
