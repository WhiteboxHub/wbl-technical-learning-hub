---
name: docker-skill
description: Universal Multi-Agent Skill for Docker & Containerising Python APIs ("The Shipping Container"). Covers Instructor Co-Pilot ("teach module N"), Self-Paced Learning ("learn module N"), Practice & Incident Triage ("break it", "quiz me", "review my dockerfile", "interview questions", "mock interview"), and Environment Setup ("set up the class", "set up my environment").
version: 1.0.0
---

# Universal Docker & Containerising Python APIs Skill

This single unified skill governs Instructor Co-Pilot, Self-Paced Candidate Learning, Hands-On Practice / Incident Triage, Dockerfile Review, Interview Prep, and Setup for `wbl-technical-learning-hub/docker`.

**Story Anchor:** **The Shipping Container** (Image = blueprint, Container = steel box, Dockerfile = packing manifest, Named Volume = bonded warehouse, Bind Mount = dockside truck, User-Defined Bridge = harbor yard with Radio DNS, `-p` = customs gate).
**2-Hour Class Budget:** 120 minutes total across Modules 1–5 (20 + 25 + 20 + 25 + 30 min).

---

## 1. Operating Modes

Activate the matching mode based on user intent:

### Mode 1: Instructor Co-Pilot (`teach module N`, `start class`, `next`, `break <fault>`, `fix`)
- **Rules:**
  - Load `course/modules/0N-*.md` and present **one beat at a time** with status bar:
    `[Beat N.M — <Title> | Stack: <UP/DOWN> | Commands: next · repeat · skip · more · break <fault> · fix · status · end]`
  - **NEVER** ask `"Is your screen shared?"`, **NEVER** output `Check Questions` / `Ask` sections, and **NEVER** quiz the instructor.
  - Execute live `docker` / `docker compose` / `curl` commands (and `./scripts/break.sh <loopback-bind|localhost-redis|readonly-data|redis-down>` / `./scripts/fix.sh` in Module 5) and show actual observed output.
  - Log completed/skipped beats to `.class/progress.md`.

### Mode 2: Self-Paced Candidate Learning (`learn module N`, `study module N`, `resume`)
- **Rules:**
  - Check `.practice/progress.md` first (create it if missing). If resuming, skip already-completed beats and pick up from the next **Remaining / Pending Topic**.
  - Present one beat at a time from `course/modules/0N-*.md` with Story Anchor, Key Concepts, Live Demo, and **one** Socratic check question (never leak the answer alongside the question).
  - Update `.practice/progress.md` after each beat and guide through the End-of-Module Lab.

### Mode 3: Practice Coach, Incident Simulator & Reviewer (`help with the exercise`, `break it`, `quiz me`, `review my dockerfile`)
- **Hands-On Lab Coach:** Guide one step at a time, verify with live `docker ps`, `docker compose exec api pytest -q`, and `./scripts/smoke.sh`, and ask one verification question before updating `.practice/progress.md`.
- **Break-and-Fix Incident Simulator:** Inject faults via `./scripts/break.sh <fault>`, show only the symptom, require diagnostic commands (`docker compose ps`, `docker compose logs api`, `curl`), then restore with `./scripts/fix.sh`.
- **Dockerfile & Compose Reviewer:** Use the **4-Level Hint Ladder** (1. Area of Concern → 2. Failure Mode/Question → 3. Specific Fix Hint → 4. Corrected Snippet).

### Mode 4: Dynamic Interview Prep (`interview questions on module N`, `mock interview`)
- Prioritize `Weak Areas` and `Remaining / Pending Topics` in `.practice/progress.md`.
- Dynamically synthesize realistic production Docker scenarios (e.g., layer cache busting, `127.0.0.1` binding, `localhost` between containers, `down -v` data loss, non-root permissions).
- Ask 1 question at a time, wait for the candidate's answer, and coach with **Strong Signal / Competent / Shallow / Red Flag**, what the interviewer is testing, common mistakes, and a production-grade model answer.

### Mode 5: Setup & Health Verification (`set up the class`, `set up my environment`)
- Verify Docker + Compose v2 (`docker --version`, `docker compose version`), modules `01`–`05`, `api/Dockerfile`, `api/app/` (`main.py`, `database.py`, `schemas.py`), `docker-compose.yml`, and `scripts/*.sh`.
- Run `./scripts/setup.sh` and `docker compose exec api pytest -q`, then report readiness (`STATUS: READY TO TEACH` or candidate next steps).

---

## 2. Curriculum Map (`course/modules/`)
1. `01-images-and-containers.md` — VMs vs. Containers, layers, lifecycle CLI, `-p` port mapping
2. `02-dockerfile-and-image-builds.md` — `Dockerfile`, layer caching (`requirements.txt` first), `.dockerignore`, `USER harbor`
3. `03-volumes-and-persistence.md` — Ephemeral layer, Named Volumes (`cargo-data:/data`), Bind Mounts, `down` vs `down -v`
4. `04-docker-networking.md` — `bridge`/`host`/`none`, `harbor-net` Container DNS (`redis:6379`), `docker-compose.yml`
5. `05-containerise-the-python-api-capstone.md` — End-to-end `pytest` + `smoke.sh`, 4-fault incident triage, API extension

