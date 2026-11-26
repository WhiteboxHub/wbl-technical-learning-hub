# Structured Step-by-Step Learning Plan (For Candidates & AI Agents)

> **To any AI Agent (ChatGPT, Claude, Antigravity, Codex, Cursor, Gemini) reading this repo:**
> When a candidate shares this repository and asks to learn MySQL & NoSQL step by step, **follow this exact 4-Module curriculum, teaching protocol, and evaluation flow**. Teach one Beat at a time, ask them to explain concepts back in their own words, and never solve lab exercises for them.

---

## How the 4-Phase AI Study Loop Works (Per Module)

### Phase 1 — Structured Topic Explanation (Tutor Mode)
1. Check `candidate-state.md` (if absent, start at Module 1 or ask which module their instructor covered).
2. Read `course/modules/01-*.md` through `04-*.md`.
3. Teach **one Beat at a time** using the 3-Act Storytelling Rule:
   - **Act 1:** 1-sentence hook + job relevance using the module's **Story Anchor**.
   - **Act 2:** Metaphor first -> exact MySQL 8.0 / architectural rule -> concrete `training_db` example.
   - **Act 3:** 3-bullet recap + the Beat's **Candidate Takeaway**.
4. **Check Understanding:** Ask the Beat's `Ask` question OR ask the candidate to explain the **Candidate Takeaway** in their own words. Wait for their reply before moving on.

### Phase 2 — Hands-On SQL Practice (Practice Mode)
1. Use `db/labs/module-01-*.sql` … `04-*.sql`, one task at a time.
2. **Prediction Rule:** Before running/checking any `SELECT`, `JOIN`, or `Window` query, make the candidate predict the row count using [docs/schema-reference.md](schema-reference.md).
3. Ask 1 follow-up "why" question before marking the task Completed.

### Phase 3 — SQL Review & Hint-First Debugging (SQL Coach Mode)
1. Compare candidate SQL privately against `db/solutions/module-01-*.sql` … `04-*.sql`.
2. Review in order: syntax/execution order -> edge cases (`NULL` traps, duplicate joins, `WHERE` vs `HAVING`, non-SARGable predicates, leftmost index column) -> readability -> 1–2 improvements.
3. Use the **4-Rung Hint Ladder** (expected vs actual -> conceptual cause -> partial SQL skeleton -> solution + follow-up query).

### Phase 4 — Evaluation, Weak-Area Diagnosis & State Update (Quiz Mode)
1. Ask **8 questions ONE at a time** mixing conceptual, "explain in your own words", scenario, and predict-row-count / `EXPLAIN` questions.
2. **NEVER reveal answers or hints while the quiz is running.**
3. **After question 8 only:** output `QUIZ RESULT` (score, per-beat breakdown, missed explanations, priority weak areas), `UPDATED CANDIDATE STATE`, and `DAILY REPORT` ([docs/student-guide.md](student-guide.md)).

---

## 4-Module Roadmap & Exit Gates

| Module | File | Topics Covered | Exit Gate (What Candidate Can Explain & Demonstrate) |
|---|---|---|---|
| **1** | `01-foundations-schema-normalization.md` | RDBMS vs flat files, SQL vs NoSQL, TCP:3306, `INT`/`VARCHAR`/`TEXT`/`DATE`/`DECIMAL`, 5 Constraints, 1NF/2NF/3NF | Connect to `training_db`, trigger/read `CHECK` & `FK` errors, normalize a flat table to 3NF |
| **2** | `02-queries-joins-ctes-windows.md` | Safe CRUD, `IS NULL`, `WHERE` vs `HAVING`, `INNER JOIN` duplicate bug, `LEFT JOIN` anti-join, `NOT EXISTS`, `WITH` / `WITH RECURSIVE`, Window Functions (`ROW_NUMBER`, `DENSE_RANK`, `LAG`, `SUM OVER`) | Fix a duplicated join, write an anti-join, walk `mentor_id` recursively, solve Top-1 per student |
| **3** | `03-transactions-locking-indexing-explain.md` | ACID & DDL implicit commit, `REPEATABLE READ` + MVCC, `FOR UPDATE` vs optimistic locking, deadlocks, Triggers & Proc trade-offs, Composite/Covering Indexes (Leftmost Prefix, SARGability), `EXPLAIN ANALYZE` + Keyset pagination | Demonstrate `ROLLBACK` & `FOR UPDATE`, verify `enrollment_log` trigger, tune `activity_log` and fix `OFFSET` |
| **4** | `04-caching-scaling-nosql-practice.md` | Redis Cache-Aside, 5-step Scaling Ladder (Read Replicas, `PARTITION BY RANGE`, Sharding), CAP & 5 NoSQL DBs (MongoDB, Redis, Neo4j, Elasticsearch, VectorDB), `scripts/break.sh` fault diagnosis + Capstone | Walk the scaling ladder, pick across MySQL + 5 NoSQL DBs, diagnose live faults, complete 3NF capstone |
| **Self-Study 1** | [01-sql-senior-deep-dive.md](../course/self-study/01-sql-senior-deep-dive.md) | `CASE WHEN`/`COALESCE`, `SELF JOIN`/`FULL JOIN` emulation/`INTERSECT`/`EXCEPT`, `LEAD`/Window frames, `VIEW` vs CTE vs Temp Table, Gap locks, **SQL Injection & Prepared Statements**, Backups & Zero-Downtime Migrations | Write conditional aggregations, explain Gap locks, fix SQL injection with Prepared Statements, plan expand-and-contract migrations |
| **Self-Study 2** | [02-nosql-complete-guide.md](../course/self-study/02-nosql-complete-guide.md) | CAP & BASE vs ACID, MongoDB (Embedding vs Referencing, CRUD, `$group`), Redis (Strings/Hashes/Sets/Sorted Sets, RDB vs AOF), Elasticsearch (`match` vs `term`, inverted index), VectorDB (RAG + filters) & Neo4j | Model MongoDB embed vs reference, run Redis Hashes/Sorted Sets, distinguish `match` vs `term`, explain VectorDB metadata filters |
