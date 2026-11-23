# Instructor steps: how to start and take the class

Course: HTTP, Web Services, REST APIs, Auth/SSO and Microservices, taught with an AI co-pilot (Claude Code) and a shared HR demo system.
Project folder: `http-course/` (inside this folder). More detail: `http-course/docs/instructor-guide.md` and `http-course/docs/class-day-quickstart.md`.

## Before class

1. **Open the right folder.** In Claude Code, open `http-course-main/http-course` (the inner folder, which holds `.claude/skills/`) and start a **new session**. Skills only load at session start.
2. **Start Docker Desktop** and wait until it says it is running.
3. **If you are teaching Module 5,** pull the images early so class is not spent waiting: `docker compose --profile sso up -d --build` (the Keycloak download is large). Then run `scripts/fix.sh`.
4. **Open your slides** (`updated_http.pdf`) on the screen you will present from.

## Starting the class

1. Say **"set up the class"**. It checks Docker and ports, starts everything, runs the smoke test, and ends with **READY** and the URLs.
2. Say **"teach module N"**, for example `teach module 1`.
3. The agent checks which parts of the stack that module needs and tells you if something is missing. It also lists the **NEW slides** to prepare, because about 65 slides are not made yet; for those it gives talking points instead.
4. It asks whether your screen is shared. If yes, answers stay hidden until you ask for them.

## Start commands by module

| Module | Start with |
|---|---|
| 1, 2, 3, 6 | `scripts/setup.sh` (the "set up the class" step) |
| 4 | `docker compose -f docker-compose.yml -f docker-compose.auth.yml up -d` |
| 5 | `docker compose --profile sso up -d --build` |
| 7 | `docker compose -f docker-compose.yml -f docker-compose.split.yml up -d --build` |
| 8 | `scripts/fix.sh`, then `scripts/break.sh <fault>` |

After Modules 4, 5, 7 or 8, run `scripts/fix.sh` to return to the normal baseline.

## During class

The agent works one beat at a time: it tells you which slide to show, gives the key points, runs or hands over the demo, and asks 1 to 3 questions. You present and talk to the room.

| You say | What happens |
|---|---|
| `next` / `back` | move between beats |
| `repeat` | re-run the demo |
| `skip` | skip it and log it |
| `answer` | reveal the answer to the question just asked |
| `more` | another question or example |
| `status` | progress and time |
| `take over` | you run the demo yourself; the agent waits |
| `jump 1.6` | go to a beat |
| `end` | wrap up |

- **Modules 1 to 7:** the agent runs most demos and you narrate. Browser demos (DevTools, the SSO login) are yours. In Module 5 you type the demo password into Keycloak yourself; the agent never reads it aloud.
- **Module 8:** run one fault at a time (`scripts/break.sh <fault>`): expired-token, wrong-role, missing-cors, rate-limit, departments-down, stale-cache. Give the room the evidence, let them diagnose, then run `scripts/fix.sh`.

## At the end of each module

1. Say `end`. The agent recaps, gives you the candidate exercise, runs the done-check (you report how the room did), and offers a reset.
2. It writes a post-class note to `.class/progress.md`: skipped beats, confusing topics, slide gaps.
3. Run `scripts/fix.sh` before the next module.

## If something goes wrong

| Problem | Do this |
|---|---|
| Docker is not running | Start Docker Desktop, then say "set up the class" again |
| Demo output looks different | Say "reset the data" (runs `scripts/setup.sh --reset`) |
| Skill not found | You are in an old session; open the inner `http-course` folder in a new one |
| Stack is stuck | `scripts/setup.sh --stop`, then `scripts/setup.sh` |
| No internet | Module 1 beat 1.9 and Module 2 beat 2.1 need it; teach those from the slides |
| Module 2: the list is empty on the page | CORS starts off on purpose; that is the demo |

## Candidates

Send them `http-course/docs/student-guide.md`. Before class they say **"set up my environment"**; afterwards they say **"quiz me"** or **"help with the exercise"**.
