# Class-Day Quick Start (Instructor — 2-Hour Class)

**What is ready:** 4 streamlined modules engineered to fit cleanly in **2 hours (120 minutes)** on a live MySQL 8.0 + Adminer + Redis stack (`Training Management DB`).

## 1. Open the repo in a NEW AI Session
Open `mysql-course/` (inside `wbl-technical-learning-hub`) in Claude Code, Antigravity, or your AI coding agent and start a **new session**.

## 2. Start Docker Desktop, then say:
> **set up the class**

Wait for **READY**. It starts MySQL (`:3306`), Adminer (`:8082`), and Redis (`:6379`), seeds `training_db`, and runs `scripts/smoke.sh`.

## 3. Say:
> **teach class** (for the full 2-hour flow) or **teach module 1** … **teach module 4**

| Module | Time Budget | Focus |
|---|---|---|
| 1 | 25 min (`0:00–0:25`) | Foundations, TCP:3306, Data Types, 5 Constraints, 3NF |
| 2 | 35 min (`0:25–1:00`) | Safe CRUD, `IS NULL`, `GROUP BY`/`HAVING`, Joins, `NOT EXISTS`, CTEs & Window Functions |
| 3 | 30 min (`1:00–1:30`) | ACID, Isolation & `FOR UPDATE`, Deadlocks, Triggers/Proc rule, Composite Index & `EXPLAIN ANALYZE` |
| 4 | 30 min (`1:30–2:00`) | Redis Cache-Aside, Partitioning vs Sharding, CAP & 5 NoSQL DBs, 2 live `scripts/break.sh` faults |

| You say | What happens |
|---|---|
| `next` / `back` | Move between beats |
| `repeat` | Re-run the SQL demo |
| `skip` | Skip beat and log it |
| `answer` | Reveal the answer to the question just asked |
| `status` | Shows beats done + **elapsed time vs 120-min budget** |
| `jump 2.3` | Jump to a specific beat |
| `end` | Wrap up + assign post-class lab |

## 4. Candidates After Class
Send candidates [docs/student-guide.md](student-guide.md) and [docs/learning-plan.md](learning-plan.md) so they can review every Beat, run the 4 labs in `db/labs/`, practice explaining concepts in their own words, and send you their Daily Report.
