# Instructor Guide — Docker & Containerising Python APIs

Taught with an AI co-pilot (Claude Code `.claude/skills/teach-docker-class`) and the **Cargo Manifest API** (`FastAPI` + `SQLite` + `Redis`) stack.

**Short on time? Check the [Class-Day Quick Start](class-day-quickstart.md).**

---

## 1. The Big Picture (How Class Runs)
- **You lead the room; the AI co-pilot handles the terminal.** You explain the *why* behind each concept and talk to students. The co-pilot keeps track of where you are, runs the live `docker` and `curl` commands, and saves notes in `.class/progress.md`.
- **Start with the real-world problem, not the tool.** Before typing any Docker command, remind students of the classic headache: *"It works on my laptop, why does it fail on my teammate's machine or in production?"* Docker solves that by shipping the app **plus** its exact Python version, libraries, and config together in one standardized box.
- **Keep Instructor Mode fast and focused:** The AI co-pilot will **not** interrupt you with screen-sharing questions or quiz you mid-class. (Quiz and practice questions are only for students using `practice-docker`.)

---

## 2. Before Class Starts (5-Minute Prep)
1. Open **Docker Desktop** and make sure it says **Running** (whale icon is steady).
2. Open the `docker/` folder in Claude Code in a **new session** so `.claude/skills/` load.
3. Run `./scripts/setup.sh` (or tell the co-pilot **"set up the class"**). Wait until you see **`== READY`**.
4. Open **http://localhost:8000/docs** in your browser so you have Swagger UI ready to show.
5. Remind students to run `./scripts/setup.sh` from the [Student Guide](student-guide.md) before class begins so you don't lose 15 minutes to downloads.

---

## 3. Running Class with the Co-Pilot
Say **"teach module 1"** (through 5) to begin. You control the pace with simple commands:

| What you say | What happens |
|---|---|
| `next` / `back` | Move forward or backward one beat |
| `repeat` | Re-run the last terminal demo |
| `skip` | Skip a beat if you're short on time (logged automatically) |
| `more` | Get another real-world example or deeper detail |
| `status` | See how much of the module is done and how time is tracking |
| `jump 2.3` | Jump straight to a specific beat |
| `end` | Finish the module and save session notes |

---

## 4. Teaching Tips That Keep the Room Engaged
- **Get a container running early:** Don't spend 20 minutes on theory before running a command. Run `docker ps` and `curl http://localhost:8000/health` early so students see something real right away.
- **Break it on purpose, then fix it:** Students remember *why* a rule matters when they see what goes wrong without it:
  - **Module 2 (Layer Caching):** Put `COPY . .` above `pip install` and edit a comment in `main.py`—students watch `pip` re-download everything. Flip the order, edit again, and watch the rebuild finish in ~1 second (`CACHED`).
  - **Module 3 (Volumes):** Save a container record, delete the container (`docker rm -f`), and show that the data is gone. Attach `cargo-data:/data` and repeat—the data survives.
  - **Module 4 (Networking):** Point `REDIS_URL` to `localhost:6379` inside the API container and show `/health` reporting `"redis": "unreachable"`. Explain that `localhost` inside a container means *that container itself*, not the laptop or another container. Switch to `redis://redis:6379/0` on `harbor-net` and watch it connect.

---

## 5. Realistic 2-Hour Class Pacing (120 Minutes)
Keep an eye on the clock—the goal is **understanding + hands-on confidence**, not memorizing every Docker flag:

| Module | Focus | Talk + Demo | Student Try-It | Total |
|---|---|---|---|---|
| **1** | Why Docker? Images vs. Containers | 15 min | 5 min | **20 min** |
| **2** | Writing a `Dockerfile` & Fast Rebuilds | 20 min | 5 min | **25 min** |
| **3** | Saving Data with Volumes & Bind Mounts | 15 min | 5 min | **20 min** |
| **4** | Container Networking & `docker compose` | 20 min | 5 min | **25 min** |
| **5** | Capstone: Testing & Fixing Broken Containers | 15 min | 15 min | **30 min** |

*Tip:* If students fall behind typing during Modules 2–4, have them run `./scripts/fix.sh` so everyone starts Module 5 from a clean, working stack.

---

## 6. Module 5: Live Debugging Drills
In the last 30 minutes, act out real production-style incidents using `./scripts/break.sh <fault>`. Have students inspect `docker ps`, `docker logs`, and `curl` to figure out what broke before you reveal the answer:

| Command | Real-World Scenario |
|---|---|
| `./scripts/break.sh loopback-bind` | *"The container says `Up`, why can't I reach port 8000 from my browser?"* (`uvicorn` bound to `127.0.0.1` instead of `0.0.0.0`) |
| `./scripts/break.sh localhost-redis` | *"The API is up, but `/health` says Redis is unreachable."* (`REDIS_URL` uses `localhost` instead of service name `redis`) |
| `./scripts/break.sh readonly-data` | *"`GET /containers` works, but `POST /containers` fails."* (`cargo-data` volume was mounted read-only `:ro`) |
| `./scripts/break.sh redis-down` | *"Everything was working, then Redis stopped responding."* (`harbor-redis` container is paused) |

Reset everything back to normal in one command:
```bash
./scripts/fix.sh
```

---

## 7. Quick Pre-Flight Checklist
- [ ] Docker Desktop is running
- [ ] `./scripts/setup.sh` printed `== READY`
- [ ] `http://localhost:8000/docs` loads in the browser
- [ ] Port `8000` is not held by another class project (like `http-course`)

---

## 8. When Something Goes Wrong in Class

| What You See | Why It Happened | How to Fix It |
|---|---|---|
| `setup.sh` says Docker isn't running (exit `11`) | Docker Desktop is closed or still starting | Open Docker Desktop, wait for it to say Running, re-run `./scripts/setup.sh` |
| `setup.sh` says port `8000` is in use (exit `12`) | Another app (often `http-course`) is using port `8000` | Run `lsof -nP -iTCP:8000 -sTCP:LISTEN` to see what it is, and stop it (`docker compose down` in that folder) |
| API won't start or smoke test fails (exit `13` / `14`) | Build error or crash on startup | Run `docker compose logs --tail 30 api` and `docker compose ps` |
| `Permission denied` writing `/data/manifest.db` | Volume or `/data` folder owned by `root` instead of `harbor` | Check `chown -R harbor:harbor /srv /data` runs before `USER harbor` in `api/Dockerfile` |
| Messy data or weird state after demos | Leftover test records or an active `break.sh` fault | Run `./scripts/fix.sh` or `./scripts/setup.sh --reset` |

**Pause for the day (keep data):** `./scripts/setup.sh --stop` · **Wipe and start fresh:** `./scripts/setup.sh --reset`

---

## 9. After Class
Check `.class/progress.md` (private to your machine, git-ignored) to see which beats took longer than expected or confused students, so you can tune the next session.
