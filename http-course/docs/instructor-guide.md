# Instructor Guide

HTTP, Web Services, REST APIs, Auth/SSO and Microservices, taught with an AI co-pilot (Claude Code) and a shared HR demo system.

**In a hurry? See the [Class-day quick start](class-day-quickstart.md).**

**Status:** All 8 modules are scripted and every demo has a working stack behind it. Setup, the teach engine and the candidate practice skill are ready. **Module 1 is fully scripted and runs end to end.** Modules 2–8 are scripted too, but many of their demos need stack components that aren't built yet (see the table below and `course/stack-backlog.md`).

---

## 1. How the course works
- **You teach; the agent co-pilots.** It keeps the plan, runs or hands over demos, holds the answer key and tracks progress. You present the slides from `updated_http.pdf` and talk to the room.
- **One example throughout:** an HR system (employees, departments, managers, salary) served at `http://localhost:8000` by a FastAPI app on Postgres, started with Docker Compose.
- **Structure:** 8 modules, each split into short *beats* (slides to show, points to say, a demo, questions with answers, an exit check).

| # | Module | Teach script | Live demos | Start with |
|---|---|---|---|---|
| 1 | HTTP foundations | ready | all | `scripts/setup.sh` |
| 2 | Websites, browser and storage | ready | all | `scripts/setup.sh` (CORS starts off) |
| 3 | JSON and REST APIs | ready | all | `scripts/setup.sh` |
| 4 | Authentication and tokens | ready | all | `docker compose -f docker-compose.yml -f docker-compose.auth.yml up -d` |
| 5 | SSO and web security | ready | all | `docker compose --profile sso up -d --build` |
| 6 | API gateway and scaling | ready | all | `scripts/setup.sh` |
| 7 | Microservices | ready | all | `docker compose -f docker-compose.yml -f docker-compose.split.yml up -d --build` |
| 8 | Capstone | ready | all six faults | `scripts/fix.sh`, then `scripts/break.sh <fault>` |

Each module file begins with a **Stack requirements** section; the agent reads it and checks it at the start of class. `scripts/fix.sh` returns to the healthy baseline after Modules 4, 5, 7 or 8.

If a component is not running (for example you forgot the `sso` profile), the agent says so at the start of the module and teaches that beat from the slides.

## 2. Before your first class (one time)
1. Install **Docker Desktop** and **Claude Code** (desktop app or CLI). Optional: Postman.
2. Get the `http-course` repo and open it in Claude Code, so the skills in `.claude/skills/` load. Start a **new session after opening the repo**; skills are picked up at session start.
3. Say **"set up the class"** (skill `setup-http-class`). It checks Docker, ports 8000 and 5432, starts the stack, and runs a 16-check smoke test. You get a READY checklist with URLs.
4. Open `updated_http.pdf` on the screen you will present from.
5. Check the module's **NEW slide** list (the agent shows it at the start). Those slides don't exist yet; the agent will tell you to teach them from talking points.

## 3. Running a class
Say **"teach module 1"** (skill `teach-http-class`).

The agent will:
1. Confirm the stack is healthy and offer to resume unfinished progress.
2. Show objectives, number of beats, estimated time, and missing slides.
3. Ask **"Is your screen shared?"** Answers are always held until you ask.
4. Run each beat: *Show slide N* → key points → demo → 1–3 questions → wait for you.

**Your controls** (plain language works too):

| Say | Effect |
|---|---|
| `next` / `back` | move between beats |
| `repeat` | re-run the demo |
| `skip` | skip and log it |
| `answer [n]` | reveal the answer to a question |
| `more` | another question or example |
| `status` | progress and time used |
| `take over` | you run a demo yourself; the agent waits |
| `jump 1.6` | go to a beat |
| `end` | wrap up |

**Demos:** each is tagged `agent` (agent runs it and you narrate) or `instructor` (agent gives the steps, you run it). The agent never advances until you say so.

**At the end** the agent recaps, gives you the candidate exercise text, walks the done-check (you tell it how the room did), offers a reset, and writes a post-class note to `.class/progress.md` (skipped beats, confusion, slide problems).

## 4. Class-day checklist
- [ ] Docker running; `setup-http-class` reports READY
- [ ] Slides open; missing slides noted
- [ ] Browser ready for DevTools demos; internet available for the TLS/caching demo (beat 1.9)
- [ ] Candidates have done `setup-candidate` (see the [Student Guide](student-guide.md)), ideally before class
- [ ] Screen sharing: decide whether answers stay hidden (default: hidden)

## 5. Module 1 at a glance (about 75–90 min)
| Beat | Topic | Demo (who) |
|---|---|---|
| 1.1 | Networking in one slide | `curl -v` connect (agent) |
| 1.2 | What HTTP is, stateless | same request twice (agent) |
| 1.3 | URI vs URL vs URN, URL anatomy | query string, percent-encoding (agent) |
| 1.4 | Anatomy of a message | raw request with `nc` (agent) |
| 1.5 | Methods, safe vs idempotent | create → read → PUT → PATCH → DELETE (agent) |
| 1.6 | Status codes | provoke 200/404/405/422/409/307 (agent) |
| 1.7 | Headers, bodies, negotiation, redirects | headers, `Accept`, `-L` (agent) |
| 1.8 | Connections and HTTP versions | keep-alive, HTTP/1.1 vs 2 (agent) |
| 1.9 | HTTPS/TLS and caching | certificate, 304 (agent, needs internet) |
| 1.10 | Cookies, auth, REST previews | none |
| 1.11 | Debugging | DevTools Network tab (**instructor**) |

Exercise (~15 min): five `curl` commands against the HR API. Done-check: five items the agent reads out and records.

## 6. Known facts about the demo API (so nothing surprises you)
- It ignores `Accept` and always returns JSON.
- A wrong `Content-Type` gets **422**, not 415.
- It does not implement `HEAD` or `OPTIONS`; wrong methods get **405** with an `allow` header.
- `GET /v2/employees/` (trailing slash) redirects with **307**.
- No authentication yet (arrives in Module 4); `salary` is visible to everyone.
- Deleting a department that still has employees returns **409**.

## 7. Troubleshooting
| Symptom | Fix |
|---|---|
| Setup says "Docker not running" (exit 11) | Start Docker Desktop, wait until it says running, re-run |
| "Port 8000/5432 in use" (exit 12) | Stop the program that holds it (the agent shows which); the agent will not kill it without asking |
| API never healthy (exit 13) / smoke test fails (exit 14) | `docker compose logs api db`; ask the agent to investigate |
| Demo output differs from the module file | Stale data from earlier demos: ask the agent to run `scripts/setup.sh --reset` |
| Skill not found | Open the repo in a **new** session; skills load at session start |
| TLS/304 demo fails | No internet: teach from slides; the agent says so |
| Windows | Use WSL2 or Git Bash for the scripts |

**Reset to seed data:** `scripts/setup.sh --reset`. **Stop:** `scripts/setup.sh --stop`.

## 8. After class
Read `.class/progress.md`: it lists skipped beats, topics that confused the room, slide gaps, and ideas to improve the module. Feed these back into the module file and the deck. The `.class/` folder is git-ignored and personal to you.

## 9. Still to do
About 65 new slides (the agent flags each "NEW slide" and gives talking points meanwhile), the students → HR rewrite of existing slides, and automated tests for the web pages and SSO apps. See [course-toc.md](course-toc.md) for the slide work per module.
