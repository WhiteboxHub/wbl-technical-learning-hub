# Instructor Steps: How to Start and Teach System Design

Course: **System Design — Scaling, Load Balancing, Caching, Queues**, taught with an AI co-pilot (`teach-system-design-class`) and a live runnable URL Shortener / System Scaling demo stack.

Project folder: `System Design/` (inside `wbl-technical-learning-hub`). More detail: `docs/instructor-guide.md` and `docs/class-day-quickstart.md`.

## Before Class

1. **Open the right folder.** In Claude Code / Antigravity, open `wbl-technical-learning-hub/System Design` (which holds `.claude/skills/`) and start a **new session**. Skills load at session start.
2. **Start Docker Desktop** and wait until the daemon is active.
3. **Verify the environment.** Say: **"set up the class"** (skill `setup-system-design-class`). It verifies ports 8080, 8000, 6379, starts the stack, runs the 10-point smoke test, and reports **READY**.

## Starting the Class

1. Say **"teach module 1"** (or module N).
2. The agent verifies the stack state and shows the module overview: objectives, beats, and key demos.
3. The agent asks: **"Is your screen shared with candidates?"**
   - If yes: All answers to questions are kept hidden until you explicitly say `answer`.

## Start Commands by Module

| Module | Topic | Start Command |
|---|---|---|
| 1 | Client-Server, Scaling & Statelessness | `scripts/setup.sh` |
| 2 | Load Balancing & Traffic Routing | `scripts/setup.sh --scale` |
| 3 | Caching & Cache Strategies (Corner Shop) | `scripts/setup.sh` |
| 4 | Message Queues & Asynchronous Decoupling | `scripts/setup.sh` |
| 5 | Database Bottlenecks & Read Replicas | `scripts/setup.sh --nocache` |
| 6 | Monolith vs. Microservices Trade-offs | `scripts/setup.sh` |
| 7 | The Repeatable 5-Step Design Method | Whiteboard / Conceptual |
| 8 | Capstone Studio & Fault Diagnosis | `scripts/fix.sh`, then `scripts/break.sh <fault>` |

After Module 2, 5, or 8, run `scripts/fix.sh` to return to the healthy single-node baseline.

## During Class

The agent works one beat at a time: it provides the story anchor point, key bullets to speak, executes live curl/load demos, and presents check questions.

| You Say | What Happens |
|---|---|
| `next` / `back` | Move forward or back one beat |
| `repeat` | Re-run the current demo |
| `answer` | Reveal the answer key for the question asked |
| `take over` | You run commands manually; the agent waits |
| `status` | Shows progress, beats remaining, and elapsed time |
| `jump N.M` | Jump directly to beat N.M |
| `end` | Concludes module, hands over candidate exercise, runs exit check |

## At the End of Each Module

1. Say `end`. The agent recaps beats completed, gives candidate exercise instructions, and runs the **Done-Check**.
2. It logs session notes into `.class/progress.md` (topics needing reinforcement, student questions).
3. Run `scripts/fix.sh` before the next module.
