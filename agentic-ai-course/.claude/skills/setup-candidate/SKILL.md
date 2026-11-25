---
name: setup-candidate
description: Candidate (student) setup for the Week 3 PM Agentic AI Engineering course. Use when a student wants to get their laptop ready for class, says "set up my environment", "I can't get the API running", or needs to reset their ClaimFlow stack. Walks them through Python setup, installs dependencies, starts ClaimFlow AI, and verifies their first API call.
---

# Candidate setup — Agentic AI Engineering PM

Get a learner from a fresh laptop to their first successful ClaimFlow AI request. Be friendly and concrete; assume they may be new to the terminal and Python virtual environments. Explain what each step does in one short sentence before running it.

## Steps

1. **Confirm Python 3.10+** is installed:
   ```bash
   python --version
   ```
   If missing or older than 3.10, tell them to install Python 3.10+ from python.org. Do not install it for them.

2. **Clone or open the repo** in the `agentic-ai-course/` directory. Then run the setup script:

   - **macOS / Linux:**
     ```bash
     bash scripts/setup.sh
     ```
   - **Windows (PowerShell):**
     ```powershell
     powershell -File scripts/setup.ps1
     ```
   Tell them the first run installs packages and can take ~1–2 minutes.

3. **If it fails, use the exit code:**

| Exit | Say this, then |
|---|---|
| 10 | "Python 3.10+ is not found on your PATH." Give them the python.org link. Do not install it for them. |
| 11 | "Package installation failed." Show the error. Check internet access. Run `pip install -r requirements.txt` manually. |
| 12 | "Port 8000 is already in use." Show what is holding the port. Ask before stopping anything. |
| 13 | "ClaimFlow API did not start in time." Read the uvicorn error output, explain the cause, fix if it is a repo issue, re-run. |
| 14 | "Smoke test failed." Show the FAIL lines, check that `claimflow/api/main.py` is unmodified, re-run. |

   On Windows without WSL2, use `scripts/setup.ps1` in PowerShell. If they are in Git Bash, the `.sh` scripts work there too.

4. **First request, together.** Once it says READY, have them run and then explain the output:
   ```bash
   curl -s http://localhost:8000/health
   ```
   Point out the `status: healthy` JSON. Then open the interactive docs:
   ```
   http://localhost:8000/docs
   ```
   Have them submit one claim via Swagger UI: `POST /api/v1/claims` with the sample payload from `docs/student-guide.md`.

5. **Run today's PM demo script** to confirm the full stack works:
   ```bash
   # Day 1 — LangGraph
   python examples/pm/01_langgraph_deep_dive.py

   # Day 2 — Tool Calling
   python examples/pm/02_react_tools_deep_dive.py

   # Day 3 — MCP & Memory
   python examples/pm/03_mcp_memory_deep_dive.py

   # Day 4 — Multi-Agent
   python examples/pm/04_multi_agent_deep_dive.py

   # Day 5 — HITL & Evaluation
   python examples/pm/05_hitl_evaluation_deep_dive.py
   ```

6. **Confirm and wrap up** with what is running, where, and how to reset or stop:
   - API base URL: `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`
   - Dashboard: `http://localhost:8000` (web UI)
   - To reset: `bash scripts/setup.sh` again (idempotent)
   - To stop: `Ctrl+C` in the terminal running uvicorn, or `docker compose down`

## Rules
- Never solve their problem silently: say what broke and what you changed.
- Do not edit `claimflow/` application code or course files just to get setup to pass.
- If they ask about class content during setup, say that comes in class — keep this skill to environment setup only.
- No paid API keys are required. ClaimFlow runs fully in mock mode out of the box.
- If a real LLM key is set via `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` and fails, explain the difference and confirm mock mode works.
- Credentials in `docker-compose.yml` are dev-only and fine to mention; never ask for or store real secrets.
