# Instructor Steps: How to Start and Teach the 2-Hour MySQL Class

Course: **MySQL & NoSQL Essentials (2-Hour Live Class + AI Self-Study)**, taught with an AI co-pilot and a shared **Training Management DB** (`training_db`).
Project folder: `mysql-course/` (inside `wbl-technical-learning-hub`). More detail: [docs/instructor-guide.md](docs/instructor-guide.md) and [docs/class-day-quickstart.md](docs/class-day-quickstart.md).

## Before class
1. **Open the right folder.** Open `wbl-technical-learning-hub/mysql-course` in Claude Code / Antigravity and start a **new session**.
2. **Start Docker Desktop** and wait until it says running.
3. **Open your slides** (`SQL & NoSQL Database Management Systems.pdf`).

## Starting the 2-hour class
1. Say **"set up the class"**. It checks Docker and ports (`3306`, `8082`, `6379`), starts MySQL 8.0 + Adminer + Redis, runs `scripts/smoke.sh`, and prints **READY**.
2. Say **"teach class"** (full 2-hour flow) or **"teach module N"** (`1`–`4`).
3. Confirm whether your screen is shared (answers stay hidden until you say `answer`).

## 2-Hour Pacing Budget
| Module | Budget | Focus |
|---|---|---|
| **1** (`0:00–0:25`) | 25 min | Foundations, TCP:3306, Types, 5 Constraints, 3NF |
| **2** (`0:25–1:00`) | 35 min | Safe CRUD, `IS NULL`, `GROUP BY`/`HAVING`, Joins, `NOT EXISTS`, CTEs & Window Functions |
| **3** (`1:00–1:30`) | 30 min | ACID, `REPEATABLE READ` + `FOR UPDATE`, Deadlocks, Triggers/Proc trade-off, Composite Index & `EXPLAIN ANALYZE` |
| **4** (`1:30–2:00`) | 30 min | Redis Cache-Aside, Partitioning vs Sharding, CAP & 5 NoSQL DBs, 2 live `scripts/break.sh` faults |

## During class controls
`next` · `back` · `repeat` · `skip` · `answer` · `more` · `status` (shows elapsed vs 120-min clock) · `take over` · `jump N.M` · `end`

## At the end of class
1. Say `end`. Assign `db/labs/` + [prompts/chatgpt-quick-prompts.md](prompts/chatgpt-quick-prompts.md) so candidates review every Beat, practice explaining the **Candidate Takeaways** in their own words, and complete the labs + 8-question quiz.
2. Run `scripts/fix.sh` (or `scripts/setup.sh --stop`) to clean up.
