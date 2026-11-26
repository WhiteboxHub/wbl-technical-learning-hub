# Student Guide — MySQL & NoSQL (2-Hour Class + AI Self-Study)

Master the high-impact MySQL & NoSQL skills taught in your 2-hour class — and use **ChatGPT, Claude, Antigravity, or any AI coding agent** afterward to practice explaining every concept clearly, write real SQL against `training_db`, and test yourself with quizzes.

---

## 1. The 4 Modules (What You Will Be Able to Explain & Build)
| # | Module | You will be able to… |
|---|---|---|
| **1** | Foundations, Setup, Types, Constraints & 3NF | Explain why RDBMS beats flat files, how SQL vs NoSQL differ, connect over TCP:3306, pick exact MySQL types, enforce 5 constraints, and normalize to 3NF |
| **2** | Queries, Joins, `GROUP BY`/`HAVING`, CTEs & Window Functions | Write safe CRUD, handle `IS NULL`, contrast `WHERE` vs `HAVING`, prevent duplicated-row joins, use `LEFT JOIN` + `NOT EXISTS`, write `WITH RECURSIVE` CTEs, and solve Top-N with `ROW_NUMBER()` |
| **3** | Transactions, Locking, Indexing & `EXPLAIN ANALYZE` | Explain ACID, `REPEATABLE READ` + MVCC, stop race conditions with `FOR UPDATE` / optimistic locking, weigh Triggers/Procedures vs app code, design Composite/Covering indexes (Leftmost Prefix, SARGability), and fix `OFFSET` pagination |
| **4** | Caching, Scaling, NoSQL & Fault Diagnosis | Trace Redis Cache-Aside, walk the 5-step Scaling Ladder (`PARTITION BY RANGE` vs Sharding vs Read Replicas), choose across 5 NoSQL DBs using CAP, and diagnose `scripts/break.sh` faults |
| **Self-Study** | [SQL Deep Dive](../course/self-study/01-sql-senior-deep-dive.md) & [NoSQL Guide](../course/self-study/02-nosql-complete-guide.md) | Master `CASE WHEN`, `LEAD`/Window frames, Views vs CTEs, Gap locks, **SQL Injection**, zero-downtime migrations, plus MongoDB, Redis data structures, Elasticsearch, VectorDB & Neo4j |

---

## 2. Get Your Laptop Ready (Optional Docker Stack)
1. Start **Docker Desktop**, then inside `mysql-course/` run:
   ```bash
   scripts/setup.sh
   ```
   (Or in Claude Code / Antigravity, say **"set up my environment"**.)
2. Run your first query: `scripts/sql.sh "SELECT id, name, price FROM course;"`
3. Open **Adminer** at `http://localhost:8082` (`Server: mysql`, `User: root`, `Pass: root`, `DB: training_db`).
   Reset anytime: `scripts/setup.sh --reset` | Stop: `scripts/setup.sh --stop`.

---

## 3. Study With ChatGPT or Any AI Coding Agent (Even Without Docker)
- **In Claude Code / Antigravity / Cursor:** say **"start learning"**, **"explain module 1"**, **"help with the exercise"**, or **"quiz me"** (`practice-mysql` loads automatically).
- **In ChatGPT / Gemini Web:** paste the GitHub link to `wbl-technical-learning-hub/mysql-course` (or upload the folder) with this copy-paste prompt:
  ```text
  Read AGENTS.md, docs/learning-plan.md, docs/schema-reference.md, course/modules/, and course/self-study/.
  Guide me through Module [1 / 2 / 3 / 4] (and course/self-study/ afterward) using the 4-stage loop:
  1. Teach ONE Beat at a time (Story Anchor -> rule -> training_db example -> Candidate Takeaway) and ask 1 check question — WAIT for my reply before advancing.
  2. Walk through db/labs/ one task at a time (make me predict row counts first; 4-Rung Hint Ladder, never give finished solutions).
  3. Run an 8-question quiz one question at a time (no answers until the end), then output my score, weak areas, and DAILY REPORT.
  ```

The AI agent follows the **4-Stage Loop**:
1. **Tutor:** Explains 1 Beat with its Story Anchor -> gives the **Candidate Takeaway** -> asks you to explain it back or answer 1 check question.
2. **Practice:** Walks you through `db/labs/module-01-*.sql` … `04-*.sql` one task at a time (predict row counts first!).
3. **SQL Coach:** Reviews your SQL using the **4-Rung Hint Ladder** (hints before solutions).
4. **Quiz & Evaluate:** Asks 8 questions one at a time (no early answers), scores you, lists weak areas, and outputs your **`DAILY REPORT`**:
   `DAILY REPORT - [Name] - [Date] | Module: __ | Labs: [Done/Partial] | Score: __/8 | Weak areas: [...] | Open Qs: [...]`

---

## 4. High-Impact SQL Cheat Sheet
```sql
-- Safe NULL check & GROUP BY / HAVING
SELECT course_id, COUNT(*) AS cnt, SUM(fee_paid) AS rev
FROM enrollment WHERE status <> 'dropped'
GROUP BY course_id HAVING COUNT(*) > 1;

-- Anti-join (unmatched rows) & safe NOT EXISTS
SELECT s.id, s.first_name FROM student s
LEFT JOIN enrollment e ON s.id = e.student_id WHERE e.id IS NULL;

-- Window Function: Top-1 per group
WITH ranked AS (
  SELECT student_id, course_id, fee_paid,
         ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY fee_paid DESC, enrollment_date ASC) AS rn
  FROM enrollment
)
SELECT * FROM ranked WHERE rn = 1;

-- Pessimistic lock inside transaction
START TRANSACTION;
SELECT id, price FROM course WHERE id = 1 FOR UPDATE;
ROLLBACK;

-- Composite Index + SARGable predicate + Keyset Pagination
CREATE INDEX idx_act_student_created ON activity_log (student_id, created_at);
EXPLAIN ANALYZE SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-02';
SELECT id, event_type FROM activity_log WHERE id > 1800 ORDER BY id LIMIT 10;
```
