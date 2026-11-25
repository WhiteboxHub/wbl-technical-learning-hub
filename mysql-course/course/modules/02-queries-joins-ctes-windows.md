# Module 2 — Querying, Joins, `GROUP BY`/`HAVING`, CTEs & Window Functions (35 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **35 minutes** (`0:25–1:00`).
Deck slides: 20–34 + Senior SQL Essentials (skip `RIGHT JOIN` / `NATURAL JOIN` / `USING` deep drills — focus on what engineers actually write daily).
Story anchor: **The Wedding Guest Lists & The Ranked Ledger** — matching two lists is `INNER JOIN`; keeping unmatched bride-side guests is `LEFT JOIN`; rolling guests into tables is `GROUP BY` and filtering tables is `HAVING`; **CTEs (`WITH`)** are named scratchpads; **Window Functions (`OVER`)** rank or sum *without* collapsing rows.
Stack requirements: `scripts/setup.sh` READY.

## Objectives
Write safe CRUD, handle `NULL` (`IS NULL`), contrast `WHERE` vs `HAVING`, fix duplicated-row joins, write `LEFT JOIN` anti-joins, avoid the `NOT IN` + `NULL` trap, write modular CTEs / `WITH RECURSIVE`, and solve top-N per group with Window Functions.

---

### Beat 2.1 — Safe CRUD, `IS NULL` & `WHERE` vs `HAVING` (9 min)
- **Slides:** 20–21, 29–34
- **Say:**
  - **Selection vs Projection:** `WHERE` filters rows; `SELECT col1, col2` picks columns.
  - **Safe `UPDATE`/`DELETE` rule:** always run `SELECT` with the exact `WHERE` first — never omit `WHERE`.
  - **`NULL` means unknown** (not `0` or `''`): `= NULL` always returns 0 rows; use `IS NULL`. Notice `COUNT(*)` counts all 8 students, while `COUNT(phone)` skips NULLs and returns 6.
  - **`WHERE` vs `HAVING`:** `WHERE` filters individual rows **before** grouping; `HAVING` filters groups **after** `GROUP BY`.
- **Demo (run: agent):**
  ```bash
  scripts/sql.sh "SELECT COUNT(*) AS total_students, COUNT(phone) AS with_phone FROM student;"
  scripts/sql.sh "SELECT course_id, COUNT(*) AS enrollments, SUM(fee_paid) AS revenue FROM enrollment WHERE status <> 'dropped' GROUP BY course_id HAVING COUNT(*) > 1 ORDER BY enrollments DESC;"
  ```
  **Point out:** `WHERE status <> 'dropped'` removes dropped enrollments *before* counting; `HAVING COUNT(*) > 1` drops Course 4 (which only had 1 active row left).
- **Candidate takeaway:** *"Use `IS NULL` (never `= NULL`), run `SELECT` before `DELETE`/`UPDATE`, and remember `WHERE` filters rows before `GROUP BY` while `HAVING` filters groups after."*
- **Ask:**
  - Q: Why does `SELECT course_id, COUNT(*) FROM enrollment WHERE COUNT(*) > 1 GROUP BY course_id;` fail? — A: Aggregates aren't computed yet during `WHERE`; put aggregate filters in `HAVING`.
- **Done when:** candidates state `WHERE` vs `HAVING` cleanly.

### Beat 2.2 — `INNER JOIN` (Duplicated-Rows Bug), `LEFT JOIN` & `NOT EXISTS` (11 min)
- **Slides:** 22–28 (focused)
- **Say:**
  - Always **predict your row count before running a JOIN**. Joining on a non-unique column silently multiplies rows and inflates sums!
  - **`LEFT JOIN` + `WHERE right.id IS NULL`:** finds unmatched records (students with 0 enrollments). Note: MySQL has no `FULL OUTER JOIN` keyword (emulate via `LEFT JOIN ... UNION ... RIGHT JOIN` if needed); `UNION` deduplicates while `UNION ALL` keeps all rows faster.
  - **`NOT IN` + `NULL` trap:** if a subquery returns even one `NULL`, `NOT IN` returns **0 rows**! Always use `NOT EXISTS`.
- **Demo (run: agent):**
  ```bash
  # Duplicated-rows bug (23 rows instead of 12!) vs correct join (12 rows)
  scripts/sql.sh "SELECT COUNT(*) AS buggy_count FROM enrollment e JOIN course c ON e.fee_paid = c.price;"
  # Anti-join: 2 students with 0 enrollments
  scripts/sql.sh "SELECT s.id, s.first_name FROM student s LEFT JOIN enrollment e ON s.id = e.student_id WHERE e.id IS NULL;"
  # NOT IN trap (0 rows!) vs NOT EXISTS fix (5 non-mentors)
  scripts/sql.sh "SELECT COUNT(*) AS not_in_trap FROM student WHERE id NOT IN (SELECT mentor_id FROM student);"
  scripts/sql.sh "SELECT s.id, s.first_name FROM student s WHERE NOT EXISTS (SELECT 1 FROM student m WHERE m.mentor_id = s.id);"
  ```
  **Point out:** `buggy_count = 23` (because two courses cost `$499`), `not_in_trap = 0` (because `mentor_id` has `NULL`), and `NOT EXISTS` returns all 5 non-mentors.
- **Candidate takeaway:** *"Predict row counts before joining, use `LEFT JOIN ... WHERE id IS NULL` for missing records, and use `NOT EXISTS` instead of `NOT IN` when NULLs are possible."*
- **Ask:**
  - Q: Your `enrollment` table has 12 rows, but joining to `course` gave 23 rows. First check? — A: Check your `ON` condition — you likely joined on a non-unique column instead of the primary/foreign key.
- **Done when:** candidates explain the duplicated-rows bug and the `NOT IN` NULL trap.

### Beat 2.3 — CTEs (`WITH`, `WITH RECURSIVE`) & Window Functions (`OVER`) (15 min)
- **Slides:** Senior SQL Essentials (MySQL 8.0+)
- **Say:**
  - **CTEs (`WITH name AS (...)`):** replace unreadable nested subqueries with clean, named top-down steps; **`WITH RECURSIVE`** walks hierarchies (`student.mentor_id`).
  - **Window Functions (`OVER (PARTITION BY ... ORDER BY ...)`):** unlike `GROUP BY` (which collapses rows), Window Functions **keep every row** while computing ranks (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), running totals (`SUM OVER`), or previous/next values (`LAG`/`LEAD`).
  - **Senior pattern (Top-N per group):** compute `ROW_NUMBER()` inside a CTE, then filter `WHERE rn = 1` outside (because `WHERE` runs before window functions).
- **Demo (run: agent):**
  ```bash
  # 1. Recursive CTE: mentor hierarchy depth
  scripts/sql.sh "WITH RECURSIVE mt AS (SELECT id, first_name, 0 AS depth, CAST(first_name AS CHAR(200)) AS chain FROM student WHERE mentor_id IS NULL UNION ALL SELECT s.id, s.first_name, mt.depth + 1, CONCAT(mt.chain, ' -> ', s.first_name) FROM student s JOIN mt ON s.mentor_id = mt.id) SELECT id, first_name, depth, chain FROM mt ORDER BY depth, id;"
  # 2. Window Function: top-1 highest-fee enrollment per student + running total
  scripts/sql.sh "WITH ranked AS (SELECT s.first_name, c.name AS course_name, e.fee_paid, ROW_NUMBER() OVER (PARTITION BY e.student_id ORDER BY e.fee_paid DESC, e.enrollment_date ASC) AS rn FROM enrollment e JOIN student s ON e.student_id = s.id JOIN course c ON e.course_id = c.id) SELECT first_name, course_name, fee_paid FROM ranked WHERE rn = 1 ORDER BY first_name;"
  ```
  **Point out:** `Alice -> Bob -> Diana -> George` (depth 3) in one query; `ROW_NUMBER() OVER (PARTITION BY student_id ...)` cleanly picks each student's top course without collapsing detail.
- **Candidate takeaway:** *"`GROUP BY` collapses rows; `OVER (PARTITION BY ...)` keeps every row. Wrap `ROW_NUMBER()` in a CTE and filter `WHERE rn = 1` for Top-N per group."*
- **Ask:**
  - Q: Given tied fees `[599, 599, 499]`, what do `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` return? — A: `1, 2, 3` / `1, 1, 3` / `1, 1, 2`.
  - Q: Why must `WHERE rn = 1` sit outside the CTE instead of inside the same `SELECT`? — A: SQL evaluates `WHERE` before window functions.
- **Done when:** candidates explain `GROUP BY` vs `PARTITION BY` and Top-N with `ROW_NUMBER()`.

---

## Post-Class Practice (Candidates)
Run `db/labs/module-02-queries-joins-windows.sql` (takes ~25 min after class).
