# Module 1 — DB Foundations, Setup, Types, Constraints & 3NF (25 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **25 minutes** (`0:00–0:25`).
Deck slides: 1–8, 11–19, 37–38 (skip legacy ISAM/network/hierarchical history trivia).
Story anchor: **The Labelled Filing Room** — spreadsheets and flat CSVs break on duplicate data, slow search, and missing locks. A relational DB is a central filing room where every drawer (table) has strict column labels (types), locks at the door (constraints), and no repeated facts (3NF).
Stack requirements: `scripts/setup.sh` READY.

## Objectives
Explain why RDBMS beats flat files, connect to `training_db` over TCP:3306, pick exact MySQL types, enforce the 5 core constraints, and normalize a table to 3NF.

---

### Beat 1.1 — Why Databases, SQL vs NoSQL & Architecture (7 min)
- **Slides:** 2, 4, 5, 7, 14
- **Say:**
  - Flat CSVs fail on 4 real problems: **redundancy** (same email in 5 files), **no integrity checks**, **slow full-file scans**, and **no safe concurrency**.
  - **SQL vs NoSQL in 1 sentence:** SQL enforces schema and multi-row ACID in the DB; NoSQL does *not* remove schema — it moves schema responsibility into your application code.
  - **Architecture:** Clients (`scripts/sql.sh`, `mysqlsh --sql`, Adminer `:8082`, Workbench) talk over **TCP/IP port `3306`** to MySQL Server (`mysqld`), which parses, optimizes, and stores `training_db`.
- **Demo (run: agent):** prove the client-server connection and verify `training_db`.
  ```bash
  scripts/sql.sh "SELECT VERSION() AS mysql_ver, DATABASE() AS db; SHOW TABLES;"
  ```
  **Point out:** 10 tables in `training_db` (`student`, `course`, `enrollment`, `enrollment_log`, `instructor`, `subject`, `users`, `contact_info`, `activity_log`).
- **Candidate takeaway:** *"MySQL Server listens on port 3306; unlike flat files, it enforces constraints, indexing, concurrency, and transactions."*
- **Ask:**
  - Q: Does choosing a schemaless NoSQL database mean your data has no schema? — A: No — schema enforcement simply moves from the DB into your app code.
- **Done when:** candidates trace client -> TCP:3306 -> MySQL Server -> table.

### Beat 1.2 — MySQL Data Types & SQL Statement Groups (8 min)
- **Slides:** 15–17, 19
- **Say:**
  - **4 SQL groups you actually use daily:** **DQL** (`SELECT`), **DML** (`INSERT`, `UPDATE`, `DELETE`), **DDL** (`CREATE`, `ALTER`, `DROP` — auto-commits!), **TCL** (`START TRANSACTION`, `COMMIT`, `ROLLBACK`), plus **DCL** (`GRANT`/`REVOKE`).
  - **Types that matter:** `INT` (`AUTO_INCREMENT PK`), `VARCHAR(n)` (variable-length string — **use `VARCHAR` in MySQL, not Oracle's `VARCHAR2`**; `CHAR(n)` is fixed-length), `TEXT` (descriptions), `DATE` (`YYYY-MM-DD`), and **`DECIMAL(10,2)` for money** (never `FLOAT`!).
- **Demo (run: agent):** show why string vs integer comparison matters.
  ```bash
  scripts/sql.sh "SELECT '10' < '2' AS varchar_sort, 10 < 2 AS int_sort;"
  ```
  **Point out:** `'10' < '2'` is `1` (true) alphabetically — storing numbers or prices as strings causes silent bugs.
- **Candidate takeaway:** *"Always store money as `DECIMAL`, whole IDs as `INT`, and strings in MySQL as `VARCHAR` (not `VARCHAR2`)."*
- **Ask:**
  - Q: Why store course prices as `DECIMAL(10,2)` instead of `FLOAT` or `VARCHAR`? — A: `FLOAT` has binary rounding errors and `VARCHAR` sorts `'9.99' > '100.00'`; `DECIMAL` is exact.
- **Done when:** candidates pick types for `id`, `email`, `price`, and `enrolled_date`.

### Beat 1.3 — The 5 Constraints & 3NF Normalization (10 min)
- **Slides:** 18, 37–38
- **Say:**
  - **5 Constraints:** `PRIMARY KEY` (unique + not null), `UNIQUE`, `NOT NULL`, `CHECK (price >= 0)`, `FOREIGN KEY` (prevents orphan child rows).
  - **Normalization in plain English:**
    - **1NF:** one value per cell (no `'555-0101, 555-0199'` CSV inside one `phone` cell).
    - **2NF + 3NF:** every non-key column depends on the **whole key, and nothing but the key** (split repeating or transitive data like `users` + `contact_info` so changing a phone or instructor email happens in one place).
- **Demo (run: agent):** trigger a `CHECK` and `FOREIGN KEY` rejection live, then compare `users_unnormalized` vs `users` + `contact_info`.
  ```bash
  scripts/sql.sh "INSERT INTO course (name, duration_weeks, price) VALUES ('Bad', -1, 100);" 2>&1 || true
  scripts/sql.sh "INSERT INTO enrollment (student_id, course_id, enrollment_date) VALUES (1, 9999, '2025-03-01');" 2>&1 || true
  scripts/sql.sh "SELECT * FROM users_unnormalized;"
  scripts/sql.sh "SELECT u.name, c.phone, c.address FROM users u JOIN contact_info c ON u.user_id = c.user_id;"
  ```
  **Point out:** MySQL rejects bad data *at the DB gate* (`3819` CHECK, `1452` FK); splitting `users` + `contact_info` fixes 1NF/3NF without duplicating `name` or `email`.
- **Candidate takeaway:** *"Constraints catch bad writes even from buggy app code; 3NF means each fact lives in one table so updates never contradict."*
- **Ask:**
  - Q: Why is storing `'555-0101, 555-0199'` in one `phone` column a 1NF violation? — A: Cells must be atomic; multi-value strings cannot be cleanly indexed or filtered.
- **Done when:** candidates explain the 5 constraints and 3NF in their own words.

---

## Post-Class Practice (Candidates)
Run `db/labs/module-01-setup-schema-3nf.sql` (takes ~15 min after class).
