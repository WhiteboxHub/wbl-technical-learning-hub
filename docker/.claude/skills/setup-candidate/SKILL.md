---
name: setup-candidate
description: Interactive onboarding for a candidate's laptop in the Docker ("The Shipping Container") course. Use when a candidate says "set up my environment", "setup candidate", or needs help getting Docker running. Checks Docker, starts the stack, verifies health + pytest, and initializes .practice/progress.md.
---

# Setup Candidate: Docker ("The Shipping Container")

Get a learner from a fresh laptop to a verified, running Cargo Manifest API stack. Be friendly, concrete, and explain what each step does in one short sentence before running it.

## Steps
1. **Check Docker Installation**:
   - Run `docker --version` and `docker compose version`.
   - If missing, direct them to install Docker Desktop (`https://www.docker.com/products/docker-desktop/`).
2. **Start & Verify the Stack**:
   - Run `./scripts/setup.sh` and explain any exit code (`11` = start Docker Desktop, `12` = port 8000 already in use).
   - Run `docker compose exec api pytest -q` to confirm containerised unit tests pass.
3. **Initialize Progress Tracker**:
   - Create `.practice/progress.md` if it does not exist yet, with sections for `Current Module`, `Modules Completed`, `Remaining / Pending Topics`, `Lab Checkpoints`, `Weak Areas`, and `Interview Focus`.
4. **Confirm & Next Steps**:
   - Show live URLs (`http://localhost:8000/docs`, `http://localhost:8000/health`).
   - Point them to `docs/student-guide.md` and tell them they can type:
     - `learn module 1` (self-paced, beat-by-beat interactive lesson with live demos & checks)
     - `help with the exercise` (guided lab coach)
     - `break it` / `incident drill` (live break-and-fix debugging)
     - `quiz me on module 1` (Socratic concept drill)
     - `interview questions on module N` / `mock interview` (dynamic senior interview)
     - `review my dockerfile` (4-level hint ladder review)
