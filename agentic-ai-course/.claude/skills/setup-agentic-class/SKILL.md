---
name: setup-agentic-class
description: Instructor setup for the Agentic AI Engineering PM course. Use when an instructor wants to prepare their machine for teaching, says "set up the class", "get ready to teach", or the ClaimFlow stack is not running. Checks prerequisites, installs Python dependencies, starts the ClaimFlow API, runs the smoke test, and reports readiness.
---

# Instructor setup — Agentic AI Engineering PM

Gets the instructor's machine ready to teach the five PM agentic AI classes. Work is driven by `scripts/setup.sh`; your job is to run it, interpret the result, and fix what you can.

## Steps

1. **Run the setup script** from the `agentic-ai-course/` root: `scripts/setup.sh`. First run installs Python packages; can take ~1 minute.

2. **Handle the exit code:**

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Ready | Go to step 3 |
| 10 | Python missing or < 3.10 | Tell the instructor to install Python 3.10+. Do not install it for them. |
| 11 | pip install failed | Show the error. Check internet access. Run `pip install -r requirements.txt` manually. |
| 12 | Port 8000 in use | Show which program holds the port. Ask before stopping anything. |
| 13 | API never became healthy | Read `uvicorn` output, explain the cause, fix if it is in this repo, re-run. |
| 14 | Smoke test failed | Show the FAIL lines, investigate against `claimflow/api/main.py`, re-run. |

3. **Check the teaching environment** (report each as ready or missing):
   - Python 3.10+: `python --version`
   - Required packages installed: `python -c "import langgraph, pydantic, fastapi; print('OK')"`
   - ClaimFlow API healthy: `curl -sf http://localhost:8000/health`
   - Today's PM demo runs: `python examples/pm/01_langgraph_deep_dive.py` (or whichever day it is)
   - pytest suite passes: `pytest tests/ -q`

4. **Report a short readiness checklist** with:
   - API URL: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - How to reset: `scripts/setup.sh --reset`
   - How to stop: stop the uvicorn process (Ctrl+C) or `docker compose down`

5. **Point to the next step:** the instructor starts a class with `teach-agentic-class`.

## Rules
- Idempotent: running again on a healthy stack is safe.
- Never print or invent API keys. The only sensitive config is optional — `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`, which the instructor provides.
- Do not modify `claimflow/` application code or `docker-compose.yml` just to get setup to pass.
- If mock mode works but real LLM fails, say so clearly — the course runs fully without real LLM keys.
