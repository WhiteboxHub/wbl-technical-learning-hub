---
name: setup-candidate
description: Candidate (student) setup for the HTTP/APIs/Auth/Microservices course. Use when a candidate wants to get their laptop ready for class, says "set up my environment", "I can't get the API running", or needs to reset their practice stack. Walks them through Docker, starts the HR stack, and makes their first request.
---

# Candidate setup

Get a learner from a fresh laptop to their first successful API call. Be friendly and concrete; assume they may be new to Docker and the terminal. Explain what each step does in one short sentence before running it.

## Steps

1. **Run `scripts/setup.sh`** from the repo root. Tell them the first run can take a few minutes because Docker downloads images.
2. **If it fails, use the exit code:**

| Exit | Say this, then |
|---|---|
| 10 | "Docker isn't installed." Give the Docker Desktop link from the output. Do not install it for them. |
| 11 | "Docker is installed but not running." Ask them to open Docker Desktop and wait until it shows running, then re-run. |
| 12 | "Something else is using port 8000 or 5432." Show what it is, and ask before stopping anything. |
| 13 / 14 | Read the logs (`docker compose logs api db`), explain in plain words, fix repo issues, re-run. If it is their machine (disk full, low memory), say so. |
| 15 | They need curl. Explain how to get it on their OS. |

   On Windows, scripts need WSL2 or Git Bash. If they are in plain PowerShell, point them to WSL2 instead of working around it.
3. **First request, together.** Once it says READY, have them run and then explain the output:
   ```bash
   curl -i http://localhost:8000/v2/employees/1
   ```
   Point out the status line, a header or two, and the JSON body. Then open `http://localhost:8000/docs` in the browser.
4. **Confirm and wrap up** with what is running, where, and how to reset (`scripts/setup.sh --reset`) or stop (`scripts/setup.sh --stop`).

## Rules
- Never solve their problem silently: say what broke and what you changed.
- Do not edit course files, answer keys or exercises while setting up.
- If they ask about class content, say that comes in class; keep this skill to environment setup.
- Credentials in `docker-compose.yml` are dev-only and fine to mention; never ask for or store real passwords.
