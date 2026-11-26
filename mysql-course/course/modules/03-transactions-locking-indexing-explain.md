# Module 3 — Transactions, Locking, Indexing & `EXPLAIN ANALYZE` (30 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **30 minutes** (`1:00–1:30`).
Deck slides: 2, 8, 35–36 + Senior Concurrency & Performance (keep Triggers practical; state Stored Procedure vs App-code rule in 2 minutes instead of writing legacy proc boilerplate live).
Story anchor: **The Vault Clerk & The Index Tab** — a transaction is a sealed envelope (`COMMIT` or `ROLLBACK`). When two clerks grab the same record at once, **Isolation & `SELECT ... FOR UPDATE`** prevent double-booking. An **Index** is the thumb-tab alphabet so MySQL doesn't read all 2,000 pages of `activity_log`.
Stack requirements: `scripts/setup.sh` READY.

## Objectives
Demonstrate ACID transactions, prevent lost updates with `REPEATABLE READ` + `FOR UPDATE` / optimistic locking, explain deadlocks and triggers, design composite/covering indexes (Leftmost Prefix & SARGability), and diagnose queries with `EXPLAIN ANALYZE` + Keyset pagination.

---

### Beat 3.1 — ACID, Isolation Levels, Locking (`FOR UPDATE`) & Deadlocks (11 min)
- **Slides:** 2, 36 + Senior Concurrency
- **Say:**
  - **ACID:** Atomicity (all or nothing), Consistency (constraints hold), Isolation (concurrent safety), Durability (survives crash). **Watch out:** DDL (`CREATE`/`ALTER`) auto-commits!
  - **MySQL InnoDB default isolation = `REPEATABLE READ`** using **MVCC** (Multi-Version Concurrency Control — plain `SELECT`s read consistent snapshots without blocking writers).
  - **Stopping Lost Updates (e.g., last seat in a course):**
    - **Pessimistic:** `START TRANSACTION; SELECT ... FOR UPDATE;` locks the row until `COMMIT`.
    - **Optimistic:** `UPDATE ... SET version = version + 1 WHERE id = 1 AND version = 3;` (check affected rows).
  - **Deadlocks:** A locks row 1 -> wants 2; B locks row 2 -> wants 1. InnoDB detects and kills one (`Error 1213`). Prevent by locking IDs in consistent ascending order and keeping transactions short (never call external HTTP APIs inside a DB transaction!).
- **Demo (run: agent):**
  ```bash
  scripts/sql.sh "SELECT @@transaction_isolation AS isolation_level;"
  scripts/sql.sh "START TRANSACTION; INSERT INTO student (first_name, last_name, email, enrolled_date) VALUES ('Tx', 'Ghost', 'tx@example.com', '2025-03-01'); ROLLBACK; SELECT COUNT(*) AS after_rollback FROM student WHERE email = 'tx@example.com';"
  scripts/sql.sh "START TRANSACTION; SELECT id, price FROM course WHERE id = 1 FOR UPDATE; COMMIT;"
  ```
  **Point out:** `after_rollback = 0`; `REPEATABLE-READ` is active; `FOR UPDATE` serializes concurrent updates to the same row.
- **Candidate takeaway:** *"InnoDB defaults to `REPEATABLE READ` with MVCC; use `FOR UPDATE` or optimistic `version` checks to stop race conditions, and lock rows in consistent order to avoid deadlocks."*
- **Ask:**
  - Q: Two requests check "1 seat left" at the same millisecond and both enroll. How do you fix it? — A: Lock the parent row with `SELECT ... FOR UPDATE` inside a transaction (or use an atomic `UPDATE ... WHERE seats > 0`).
- **Done when:** candidates explain `FOR UPDATE` vs optimistic locking and one deadlock prevention rule.

### Beat 3.2 — Triggers & Stored Routines Trade-Off (5 min)
- **Slides:** 35
- **Say:**
  - **Triggers (`BEFORE`/`AFTER`, `NEW`/`OLD`):** fire automatically on `INSERT`/`UPDATE`/`DELETE`. Great for immutable audit trails (`trg_after_enrollment_insert` -> `enrollment_log`), risky if abused for heavy business logic (hidden side effects, slower writes).
  - **Stored Procedures & Functions (1-min rule):** `CREATE FUNCTION` returns a scalar inside `SELECT`; `CREATE PROCEDURE` runs multi-step SQL via `CALL`. Modern teams **keep business logic in app code** (easy Git diff, unit tests, cheap horizontal scaling) and reserve DB routines for legacy maintenance or tight bulk data jobs.
- **Demo (run: agent):** verify our live audit trigger fires automatically, then clean up.
  ```bash
  scripts/sql.sh "INSERT INTO enrollment (student_id, course_id, enrollment_date, status, fee_paid) VALUES (7, 1, '2025-03-01', 'active', 499.00);"
  scripts/sql.sh "SELECT id, student_id, course_id, action_type FROM enrollment_log ORDER BY id DESC LIMIT 2;"
  scripts/sql.sh "DELETE FROM enrollment WHERE student_id = 7 AND course_id = 1; DELETE FROM enrollment_log WHERE student_id = 7 AND course_id = 1;"
  ```
  **Point out:** `enrollment_log` updated automatically without any extra `INSERT`.
- **Candidate takeaway:** *"Use triggers sparingly for audit logs; keep business rules in version-controlled app code where scaling and testing are cheap."*
- **Ask:**
  - Q: Why do modern microservice teams prefer app code over complex Stored Procedures for business logic? — A: App containers scale horizontally much cheaper than DB CPU, and app code supports unit tests, Git reviews, and CI/CD.
- **Done when:** candidates state the trigger/procedure trade-off cleanly.

### Beat 3.3 — Composite Indexing, SARGability & `EXPLAIN ANALYZE` + Pagination (14 min)
- **Slides:** 2, 8 + Senior Performance Tuning
- **Say:**
  - **Clustered PK vs Secondary B-Tree Index:** InnoDB stores rows inside the PK tree; secondary indexes point to PKs — unless it's a **Covering Index (`Extra: Using index`)**.
  - **Leftmost-Prefix Rule:** `INDEX (student_id, created_at)` speeds up `WHERE student_id = ?` and `WHERE student_id = ? AND created_at >= ?`, **NOT** `WHERE created_at >= ?` alone!
  - **SARGability:** wrapping an indexed column in a function (`YEAR(created_at) = 2025`) **kills the index** — always keep columns bare (`created_at >= '2025-01-01' AND created_at < '2026-01-01'`).
  - **`EXPLAIN` vs `EXPLAIN ANALYZE` + Pagination + N+1:** `EXPLAIN ANALYZE` runs the query and prints real timing/rows. Replace slow deep `OFFSET` (`LIMIT 10 OFFSET 1800`) with **Keyset Pagination** (`WHERE id > 1800 ORDER BY id LIMIT 10`), and avoid **N+1 loops** in app code by fetching via `JOIN` or `IN (...)`.
- **Demo (run: agent):** run on our 2,000-row `activity_log` table!
  ```bash
  scripts/sql.sh "EXPLAIN ANALYZE SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-02';"
  scripts/sql.sh "CREATE INDEX idx_act_student_created ON activity_log (student_id, created_at);"
  scripts/sql.sh "EXPLAIN ANALYZE SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-02';"
  scripts/sql.sh "EXPLAIN SELECT id FROM activity_log WHERE student_id = 3 AND YEAR(created_at) = 2025;"
  scripts/sql.sh "EXPLAIN ANALYZE SELECT id, event_type FROM activity_log WHERE id > 1800 ORDER BY id LIMIT 10;"
  scripts/sql.sh "DROP INDEX idx_act_student_created ON activity_log;"
  ```
  **Point out:** Before index: full table scan (`2000` rows). After index: covering index range scan! With `YEAR(created_at)`, range scan disappears (`Using where; Using index` scans all of student 3's rows). Keyset `WHERE id > 1800` touches only `10` rows.
- **Candidate takeaway:** *"Match composite indexes to `(equality_col, range_or_sort_col)` (Leftmost Prefix), never wrap indexed columns in functions (SARGable), and use Keyset pagination over deep `OFFSET`."*
- **Ask:**
  - Q: Why does `INDEX (student_id, created_at)` fail to help `WHERE created_at > '2025-01-01'`? — A: It violates the Leftmost-Prefix Rule (`student_id` is missing).
  - Q: Why is `WHERE id > 1800 LIMIT 10` faster than `LIMIT 10 OFFSET 1800`? — A: `OFFSET` reads and discards 1,800 rows; Keyset jumps directly to `id > 1800` via the PK index.
- **Done when:** candidates read `EXPLAIN ANALYZE` and fix a non-SARGable or deep-`OFFSET` query.

---

## Post-Class Practice (Candidates)
Run `db/labs/module-03-transactions-locking-indexes.sql` (takes ~20 min after class).
