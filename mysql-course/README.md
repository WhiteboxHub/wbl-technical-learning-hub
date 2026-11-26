# MySQL & NoSQL Essentials — 2-Hour Class + AI Self-Study Repo

Running example: **Training Management DB** (`student`, `course`, `subject`, `enrollment`, `enrollment_log`, `instructor`, `users`, `contact_info`, `activity_log`) — optimized for **Instructors** (a tight **2-hour live class** with zero filler) and **Candidates** (step-by-step study, concept explanation practice, SQL coaching, and quizzes in **ChatGPT, Claude, Antigravity, Codex, Cursor, or any AI agent**).

---

## Guides & Learning Roadmap
- **[Structured Learning Plan](docs/learning-plan.md)** — 4-stage AI study loop, prediction rules, evaluation, and exit gates
- **[Student Guide](docs/student-guide.md)** — laptop setup, senior SQL cheat sheet, and AI self-study flow
- **[Schema Reference](docs/schema-reference.md)** — ER diagram, table columns, and exact seed row counts
- **[Course Table of Contents](docs/course-toc.md)** — 2-hour module budget + what was kept vs trimmed
- **[Instructor Guide](docs/instructor-guide.md)** & **[Class-Day Quick Start](docs/class-day-quickstart.md)** — 5-minute setup and 120-minute live pacing controls

---

## Paste Into ChatGPT or Any AI Coding Agent (Candidates)
1. Open in **Claude Code / Antigravity / Cursor** (loads `.claude/skills/practice-mysql/SKILL.md` automatically) OR paste the GitHub link / folder into **ChatGPT / Claude Web / Gemini** with the starter prompt in **[docs/student-guide.md](docs/student-guide.md)**.
3. The AI agent will:
   - Explain each Beat clearly using its **Story Anchor**, `training_db` example, and plain-English **Candidate Takeaway**
   - Ask you to explain concepts back in your own words before moving on
   - Coach your SQL in `db/labs/` using the **4-Rung Hint Ladder** (hints before solutions)
   - Quiz you one question at a time, diagnose weak areas, and output your **`CANDIDATE STATE`** + **`DAILY REPORT`**

---

## Start the Local MySQL Lab Stack (Optional / Recommended for Hands-On SQL)
Requires **Docker Desktop** running.

```bash
scripts/setup.sh
```

- **MySQL 8.0:** `localhost:3306` (`database: training_db`, `user: root`, `password: root`)
- **Adminer (Web SQL GUI):** http://localhost:8082 (`System: MySQL`, `Server: mysql`, `Username: root`, `Password: root`, `Database: training_db`)
- **Redis (Module 4 cache-aside lab):** `localhost:6379`
- **Quick SQL command:** `scripts/sql.sh "SELECT id, name, price FROM course;"`
- **Reset to seed data:** `scripts/setup.sh --reset` | **Stop:** `scripts/setup.sh --stop`

---

## 2-Hour Course Modules (4 Focused Modules = 120 Minutes)
| # | Module | 2-Hr Budget | Key High-Impact Topics |
|---|---|---|---|
| 1 | [Foundations, Setup, Types, Constraints & 3NF](course/modules/01-foundations-schema-normalization.md) | 25 min | RDBMS vs CSVs, SQL vs NoSQL, TCP:3306, `INT`/`VARCHAR`/`TEXT`/`DATE`/`DECIMAL`, 5 constraints, 1NF/2NF/3NF |
| 2 | [Queries, Joins, `GROUP BY`/`HAVING`, CTEs & Window Functions](course/modules/02-queries-joins-ctes-windows.md) | 35 min | Safe CRUD, `IS NULL`, `WHERE` vs `HAVING`, `INNER JOIN` duplicate bug, `LEFT JOIN` anti-join, `NOT EXISTS`, `WITH RECURSIVE`, `ROW_NUMBER`/`RANK`/`DENSE_RANK`/`LAG`/`SUM OVER` |
| 3 | [Transactions, Locking, Indexing & `EXPLAIN ANALYZE`](course/modules/03-transactions-locking-indexing-explain.md) | 30 min | ACID, `REPEATABLE READ` + MVCC, `FOR UPDATE` vs optimistic locking, deadlocks, Triggers & Proc trade-off, Composite/Covering Indexes (Leftmost Prefix, SARGability), `EXPLAIN ANALYZE` + Keyset pagination |
| 4 | [Caching, Scaling, NoSQL & Live Fault Check](course/modules/04-caching-scaling-nosql-practice.md) | 30 min | Redis cache-aside, 5-step Scaling Ladder (Read Replicas, `PARTITION BY RANGE`, Sharding), CAP & 5 NoSQL DBs (MongoDB, Redis, Neo4j, Elasticsearch, VectorDB), `scripts/break.sh` faults |

### Post-Class Candidate Self-Study (Outside the 2-Hour Live Clock)
- **[Self-Study 1: Senior SQL Deep Dive](course/self-study/01-sql-senior-deep-dive.md)** — `CASE WHEN`/`COALESCE`, `SELF JOIN`/`INTERSECT`/`EXCEPT`, `LEAD`/Window frames, `VIEW` vs CTE vs Temp Table, Gap locks, **SQL Injection & Prepared Statements**, `mysqldump` & zero-downtime migrations.
- **[Self-Study 2: High-ROI NoSQL Guide](course/self-study/02-nosql-complete-guide.md)** — CAP theorem, MongoDB (Embedding vs Referencing, CRUD, `$group`), Redis (Strings/Hashes/Sets/Sorted Sets, RDB vs AOF), Elasticsearch (`match` vs `term`), VectorDB (RAG + metadata filters), and Neo4j Cypher recognition.

---

## Layout
```text
mysql-course/
├── AGENTS.md                  # Universal AI instructions (ChatGPT, Codex, Antigravity, Cursor, Claude)
├── CLAUDE.md                  # Claude Code entrypoint
├── instructor-steps.md        # 2-hour instructor runbook & pacing controls
├── docker-compose.yml         # MySQL 8.0 (:3306) + Adminer (:8082) + Redis (:6379)
├── .claude/skills/            # setup-mysql-class, teach-mysql-class (2-hr timer), setup-candidate, practice-mysql
├── course/
│   ├── modules/               # 4 tight 2-hour modules (Story Anchors, Candidate Takeaways, Demos, Q&As)
│   └── self-study/            # High-ROI post-class SQL & NoSQL self-study packs
├── db/
│   ├── init/                  # 01-schema.sql & 02-seed.sql (Training Management DB + 2,000 activity rows)
│   ├── labs/                  # 4 post-class SQL lab starters (including Capstone extension)
│   └── solutions/             # 4 separated reference solutions (never shown before attempt)
├── scripts/                   # setup.sh, smoke.sh, sql.sh, break.sh, fix.sh
└── docs/                      # learning-plan, schema-reference, course-toc, instructor & student guides
```
