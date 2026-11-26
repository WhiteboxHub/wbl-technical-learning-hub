# Instructor Steps: How to Start and Teach the Docker Course

Course: **Docker — Images, Containers, Dockerfile, Volumes, Networking & Containerising the Python API**  
Anchor Story: **The Shipping Container**  
Project Folder: `wbl-technical-learning-hub/docker`

---

## 1. Before Class (Instructor Checklist)
1. **Open the correct workspace**:
   - Open `wbl-technical-learning-hub/docker` in Antigravity / Claude Code so `.claude/skills/` load automatically.
2. **Verify Docker & Stack**:
   - Ensure Docker Desktop is running (`docker info`).
   - Run `set up the class` in chat (or manually test `docker compose up --build -d && ./scripts/smoke.sh`).

---

## 2. Starting the Class with the AI Co-Pilot
1. Type: **`setup docker class`** or **`set up the class`**
   - The agent verifies Docker availability, modules, API files, and skills readiness.
2. Type: **`teach module N`** (e.g., `teach module 1`).
3. The co-pilot **never** asks about screen sharing, **never** outputs `Ask` / `Check Questions` sections, and **never** quizzes the instructor. (Topic-wise check questions are only asked to candidates in candidate mode.)

---

## 3. Teaching Commands Reference
- `next`: Advance to the next beat
- `back`: Return to the previous beat
- `repeat`: Re-explain the current concept or re-run the demo
- `skip`: Skip the current beat
- `more`: Provide an additional Shipping Container analogy or scenario
- `status`: Show current progress and completed beats
- `take over`: Pause AI co-pilot while you lead an open discussion
- `jump N.M`: Jump directly to a specific beat (e.g., `jump 3.2`)
- `end`: Conclude the module and present the End-of-Module Lab

---

## 4. Module Teaching Overview
- **Module 1 (Images & Containers)**: Break-bulk vs ISO shipping containers; VMs vs Containers; Read-only Image vs Writable Container; `run`, `ps`, `logs`, `exec`, `stop`, `rm`, `-p`.
- **Module 2 (Dockerfile & Builds)**: `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `EXPOSE`, `USER`, `CMD`; Layer caching (`requirements.txt` before `app/`); `.dockerignore`; `python:3.12-slim` & `--host 0.0.0.0`.
- **Module 3 (Volumes & Persistence)**: Ephemeral container trap; Named Volumes (`cargo-data:/data`); Bind Mounts (`./api/app:/srv/app`) for live dev reload; `tmpfs` & `:ro`.
- **Module 4 (Docker Networking)**: `bridge` vs `host` vs `none`; User-defined bridge DNS vs default bridge; the `localhost` trap; `docker-compose.yml` (`api` + `redis` on `harbor-net`).
- **Module 5 (Capstone: Containerise the Python API)**: End-to-end build, `pytest` in container, `smoke.sh`, and 4 classic incident triage drills.
