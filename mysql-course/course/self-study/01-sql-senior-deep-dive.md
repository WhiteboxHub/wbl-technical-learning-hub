# Self-Study 1 — High-ROI Senior SQL Deep Dive (Post-Class)

> **For Candidates & AI Agents:** Study this **after** completing Modules 1–4. These are the high-value SQL topics that did not fit into the 2-hour live class but show up constantly in senior engineering work and interviews. Low-value trivia is intentionally excluded.

---

### S1.1 — Everyday SQL Expressions (`CASE WHEN`, `COALESCE`, Dates)
- **Why it matters:** Reporting and backend queries constantly transform raw values or replace `NULL`s cleanly without pulling rows into Python/Java first.
- **Key patterns on `training_db`:**
  - `COALESCE(phone, 'Not Provided')` returns the first non-NULL argument (standard SQL; `IFNULL(a, b)` is MySQL-specific).
  - `CASE WHEN price >= 500 THEN 'Premium' WHEN price >= 400 THEN 'Standard' ELSE 'Starter' END` enables conditional bucketing and **conditional aggregation** (`SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)`).
  - Date arithmetic: `DATEDIFF(CURDATE(), enrolled_date)`, `DATE_FORMAT(enrolled_date, '%Y-%m')`.
- **Try it:**
  ```sql
  SELECT
      c.name,
      COUNT(e.id) AS total_enrollments,
      SUM(CASE WHEN e.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
      SUM(CASE WHEN e.status = 'dropped' THEN 1 ELSE 0 END) AS dropped_count
  FROM course c
  LEFT JOIN enrollment e ON c.id = e.course_id
  GROUP BY c.id, c.name;
  ```
- **Check Q:** How can you count `completed` and `dropped` enrollments side by side in a single `GROUP BY` query without two separate subqueries? — **A:** Conditional aggregation using `SUM(CASE WHEN status = '...' THEN 1 ELSE 0 END)`.

---

### S1.2 — `SELF JOIN`, `FULL OUTER JOIN` Emulation & Set Ops (`INTERSECT`, `EXCEPT`)
- **Why it matters:** `LEFT JOIN` handles 90% of outer joins, while `SELF JOIN` handles hierarchical tables (`student.mentor_id`) and `UNION` / `INTERSECT` / `EXCEPT` compare two result sets vertically.
- **Key rules:**
  - **`SELF JOIN`:** join a table to itself with two aliases (`student s LEFT JOIN student m ON s.mentor_id = m.id`).
  - **`FULL OUTER JOIN` in MySQL:** MySQL 8.0 has no `FULL OUTER JOIN` keyword; emulate with `LEFT JOIN ... UNION ... RIGHT JOIN`.
  - **Set operations (MySQL 8.0.31+):** `UNION` (deduplicates), `UNION ALL` (faster, keeps all), `INTERSECT` (in both), `EXCEPT` (in first, not second). Avoid `NATURAL JOIN` in production (schema changes break it silently).
- **Try it:**
  ```sql
  SELECT s.first_name AS student, COALESCE(m.first_name, 'None') AS mentor
  FROM student s
  LEFT JOIN student m ON s.mentor_id = m.id
  ORDER BY s.id;

  SELECT name FROM course INTERSECT SELECT name FROM subject;
  SELECT name FROM course EXCEPT SELECT name FROM subject;
  ```
- **Check Q:** Why does `UNION ALL` run faster than `UNION`? — **A:** `UNION` runs an extra sort/hash pass to remove duplicates; `UNION ALL` appends rows directly.

---

### S1.3 — Advanced Window Functions (`LEAD`, `FIRST_VALUE`, Window Frames)
- **Why it matters:** Senior SQL questions love time-series comparisons ("difference from previous order", "3-row moving average", "first vs latest value per user").
- **Key pattern:** `OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)`.
- **Try it:**
  ```sql
  SELECT
      enrollment_date,
      fee_paid,
      LEAD(fee_paid) OVER (ORDER BY enrollment_date, id) AS next_fee,
      AVG(fee_paid) OVER (
          ORDER BY enrollment_date, id
          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
      ) AS moving_avg_3
  FROM enrollment
  WHERE status <> 'dropped';
  ```
- **Check Q:** What is the difference between `LAG()` and `LEAD()`? — **A:** `LAG()` looks backward at a prior row in the window; `LEAD()` looks forward at a subsequent row.

---

### S1.4 — `VIEW` vs CTE vs Derived Table vs Temporary Table
- **Decision table (what senior interviewers expect):**
  | Construct | Stored in DB? | Best Used When | Watch Out |
  |---|---|---|---|
  | **CTE (`WITH`)** | No (single query) | Breaking complex SQL into readable top-down steps, or `WITH RECURSIVE` | Usually not indexed separately |
  | **`VIEW`** | Yes (saved SQL definition) | Sharing a standard reporting query or hiding sensitive columns (`salary`/`phone`) | A View holds no data itself (in MySQL, no native materialized views) — slow underlying queries stay slow |
  | **`TEMPORARY TABLE`** | Session-scoped only | Multi-step ETL/analytics on millions of intermediate rows where you need `CREATE INDEX` on the temp result | Lives only for the current DB connection |
- **Check Q:** Does creating a standard MySQL `VIEW` make a slow `JOIN` query faster? — **A:** No — a `VIEW` is just a saved query definition (not precomputed data), so it still runs the underlying query each time.

---

### S1.5 — Full Isolation Matrix, Gap Locks & `READ COMMITTED` vs `REPEATABLE READ`
- **The 4 SQL Isolation Levels & Anomalies:**
  | Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Notes |
  |---|---|---|---|---|
  | `READ UNCOMMITTED` | Possible | Possible | Possible | Almost never used |
  | `READ COMMITTED` | Prevented | Possible | Possible | Common in Postgres/Oracle; **fewer gap locks** in MySQL |
  | `REPEATABLE READ` (**MySQL InnoDB default**) | Prevented | Prevented | Prevented (on locking reads via Next-Key locks) | Uses **MVCC snapshots** for plain `SELECT`s |
  | `SERIALIZABLE` | Prevented | Prevented | Prevented | Highest locking, lowest throughput |
- **Why 10-year engineers care about Gap / Next-Key Locks:**
  - In InnoDB `REPEATABLE READ`, `SELECT ... WHERE course_id = 1 FOR UPDATE` locks not only matching rows, **but also the gaps** around them to stop phantom inserts. Under heavy concurrent writes, gap locks can trigger deadlocks — which is why high-write services sometimes switch to `READ COMMITTED` (combined with row-level `FOR UPDATE` or optimistic `version` checks).
- **Check Q:** Why do some high-concurrency MySQL services intentionally switch from `REPEATABLE READ` to `READ COMMITTED`? — **A:** To eliminate most InnoDB gap locks on range/non-unique scans and reduce lock contention/deadlocks (while still using `FOR UPDATE` or optimistic locking where needed).

---

### S1.6 — SQL Injection & Prepared Statements *(Critical Security Skill)*
- **The exploit:** String-concatenating user input into SQL (`"SELECT * FROM student WHERE email = '" + user_input + "'"`). If `user_input` is `' OR '1'='1`, the query dumps the entire table (or worse with stacked statements).
- **The ONLY real fix:** **Parameterized Queries / Prepared Statements** (`cursor.execute("SELECT * FROM student WHERE email = %s", (email,))`). The DB compiles the SQL structure first and treats the parameter strictly as data, never executable SQL!
- **Note on `LIKE` / `ORDER BY`:** Parameters work for *values*; for dynamic `ORDER BY` columns, validate against an explicit **allowlist** (`{"name", "price", "enrolled_date"}`) in app code.
- **Check Q:** Why is escaping quotes manually worse than using Prepared Statements? — **A:** Manual escaping is error-prone across encodings and edge cases; Prepared Statements separate SQL syntax from data at the protocol/parser level.

---

### S1.7 — Backups (`mysqldump`) & Zero-Downtime Schema Migrations
- **Consistent Non-Blocking Backup:**
  ```bash
  mysqldump --single-transaction --routines --triggers -uroot -proot training_db > backup.sql
  ```
  `--single-transaction` uses an InnoDB MVCC snapshot so reads/writes continue without locking tables!
- **Zero-Downtime Migrations (Why `ALTER TABLE` breaks production):**
  - Adding a `NOT NULL` column with table rebuilds or dropping a column directly on a 50M-row table can hold metadata/table locks and break old running app instances during rolling deploys.
  - **Expand-and-Contract pattern:** (1) Add the new column as `NULL`able (`ALGORITHM=INPLACE, LOCK=NONE` when supported), (2) deploy code that writes both/handles both, (3) backfill in small batches, (4) drop the old column in a later deploy.
- **Check Q:** What flag in `mysqldump` takes a consistent InnoDB backup without locking all tables for writes? — **A:** `--single-transaction`.

---

### S1.8 — Stored Procedures vs Functions vs Triggers (Syntax Quick-Check)
- **Why Module 3 warned against heavy DB business logic:** Putting pricing/auth workflows inside Procedures hides logic from Git diffs/unit tests and strains DB CPU. Still, candidates must recognize the 3 objects cleanly:
  - **Stored Procedure (`CALL`):** accepts `IN` / `OUT` parameters, can run transactions and return result sets, cannot be called inside a `SELECT` expression.
  - **Function (`SELECT fn(...)`):** returns a single scalar value cleanly inside queries; marked `DETERMINISTIC` / `READS SQL DATA` in MySQL 8.0 (`CREATE FUNCTION fn_discount(p DECIMAL(10,2)) RETURNS DECIMAL(10,2) DETERMINISTIC RETURN ROUND(p * 0.9, 2);`).
  - **Trigger (`BEFORE`/`AFTER INSERT|UPDATE|DELETE`):** fires automatically per row (e.g., `trg_after_enrollment_insert` auditing to `enrollment_log`).
- **Syntax reference:**
  ```sql
  DELIMITER //
  CREATE PROCEDURE sp_student_summary(IN p_student_id INT)
  BEGIN
      SELECT s.first_name, COUNT(e.id) AS course_count, COALESCE(SUM(e.fee_paid), 0) AS total_paid
      FROM student s LEFT JOIN enrollment e ON s.id = e.student_id
      WHERE s.id = p_student_id GROUP BY s.id, s.first_name;
  END //
  DELIMITER ;
  CALL sp_student_summary(1);
  DROP PROCEDURE IF EXISTS sp_student_summary;
  ```
- **Check Q:** When does a **Function** make more sense than a **Stored Procedure** (and when does application code beat both)? — **A:** Use a Function for a small deterministic scalar calculation inside `SELECT`; use a Procedure only when an action must stay atomic next to the data; keep evolving business workflows in application code.

---

## Self-Study Quiz Bank (For AI Quiz Mode)
1. Rewrite a slow `SUM` across 2 statuses without running two queries (`CASE WHEN`).
2. Why does a MySQL `VIEW` not cache query results?
3. Contrast `READ COMMITTED` vs `REPEATABLE READ` regarding gap locks.
4. Explain how `' OR '1'='1` exploits string-concatenated SQL and why Prepared Statements stop it.
5. Why should a rolling deployment add a new column as `NULL`able first (Expand-and-Contract)?
6. What happens if you run `mysqldump` on a busy production InnoDB DB *without* `--single-transaction`?
7. How does calling a Stored Procedure differ from calling a Stored Function in MySQL, and why should most business logic live in application code?
