---
name: setup-ml-class
description: Instructor setup for Week 2 PM Production ML course. Use when the instructor says "set up the class", "get ready to teach", or the MLflow/Fraud API stack is not running. Checks prerequisites, prepares starter data/model, starts the stack, runs smoke checks, and reports readiness.
---

# Instructor Setup — Week 2 PM Production ML

Gets the instructor's machine ready to teach Mon–Fri. Driven by `scripts/setup.sh` (macOS/Linux/Git Bash) or `scripts/setup.ps1` (Windows PowerShell).

## Steps
1. Ask if they want **Docker stack** (default: MLflow `:5000` + Fraud API `:8000`) or **local `.venv`** (`--local` / `-Local`).
2. Run `scripts/setup.sh` (or `powershell -File scripts/setup.ps1`).
3. Check readiness:
   - `curl -sf http://localhost:8000/health` returns `{"status":"ok",...}`
   - `curl -sf http://localhost:5000/health` returns 200 (when Docker/MLflow server is up)
   - `docs/course-toc.md` and `course/modules/` exist
4. Report URLs (Fraud Console `http://localhost:8000`, Swagger `http://localhost:8000/docs`, MLflow UI `http://localhost:5000`) and how to reset (`scripts/fix.sh` / `scripts/fix.ps1`) or stop (`scripts/setup.sh --stop`).

## Rules
- Idempotent: safe to re-run on a healthy stack.
- Never kill a port-holding process without explicit instructor permission.
- Never fabricate test output; report actual smoke check output.
