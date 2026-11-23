# Class-day quick start (instructor, 5 minutes)

**What is ready:** all 8 modules, each with a working stack for its demos. Each module needs a different start command (table below); the agent checks it for you.

## 1. Open the repo in a NEW Claude Code session
Open the `http-course` folder, then start a **new session** in it. Skills load only at session start.

## 2. Start Docker Desktop, then say
> **set up the class**

Wait for **READY**. It starts the API (`:8000`), the HR Directory page (`:3000`) and Postgres, and runs a smoke test. If it stops with an error, the message says what to fix (Docker not running, port in use, and so on).

## 3. Open your slides
`updated_http.pdf` on your presenting screen. The agent tells you which slide numbers to show. **Missing slides** are flagged "NEW slide": teach those from the agent's key points.

## 4. Say
> **teach module 1**

(or `teach module 2`, `teach module 3`). The agent asks whether your screen is shared, then runs it beat by beat.

| You say | What happens |
|---|---|
| `next` / `back` | move beats |
| `repeat` | re-run the demo |
| `skip` | skip, logged |
| `answer` | reveal the answer to the question just asked |
| `more` | another question or example |
| `status` | progress and time |
| `take over` | you run the demo, agent waits |
| `jump 1.6` | go to a beat |
| `end` | wrap up with exercise and done-check |

## Start commands by module
| Module | Start with |
|---|---|
| 1, 2, 3, 6 | `scripts/setup.sh` (the "set up the class" skill does this) |
| 4 | `docker compose -f docker-compose.yml -f docker-compose.auth.yml up -d` |
| 5 | `docker compose --profile sso up -d --build` (first Keycloak pull is large; do it before class) |
| 7 | `docker compose -f docker-compose.yml -f docker-compose.split.yml up -d --build` |
| 8 | `scripts/fix.sh` then `scripts/break.sh <fault>` |
After Modules 4, 5, 7 or 8, run `scripts/fix.sh` to return to the normal baseline.

## 5. Candidates
Send them the [Student Guide](student-guide.md). Before class they say **"set up my environment"**. After class they can say **"quiz me"** or **"help with the exercise"** (skill `practice-http`).

## 6. If something goes wrong
| Problem | Do this |
|---|---|
| Demo output looks different | say "reset the data" → `scripts/setup.sh --reset` |
| Docker is not running | start Docker Desktop, say "set up the class" again |
| Stack stuck | in a terminal: `scripts/setup.sh --stop`, then `scripts/setup.sh` |
| Skill not found | you are in an old session; start a new one in the repo |
| No internet (Module 1 beat 1.9, Module 2 beat 2.1) | teach from the slides; the agent says so |
| Module 2: list is empty on the page | CORS is off on purpose at the start; that is the demo. To fix it: `docker compose -f docker-compose.yml -f docker-compose.cors.yml up -d` |

## 7. After class
`.class/progress.md` has what you skipped, what confused the room, and slide gaps. Run `scripts/setup.sh --stop` to shut Docker down.
