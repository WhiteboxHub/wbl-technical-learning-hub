---
name: setup-genai-class
description: Instructor setup for the Generative AI & RAG course (Week 3 AM). Use when an instructor wants to prepare their machine for teaching, says "set up the class", "get ready to teach", or the demo stack is not running. Checks prerequisites (Docker, curl, ports 8000, 8001, 8501, OPENAI_API_KEY), starts the stack with Docker Compose, runs the smoke test, and reports readiness.
---

# Instructor Setup

Prepares the instructor's workstation for delivering Week 3 AM (GenAI & RAG). The setup logic is managed by `scripts/setup.sh`; this skill invokes the script, diagnoses failures, and validates readiness.

## Steps

1. **Run the setup script** from the `genai-course` folder:
   ```bash
   scripts/setup.sh
   ```
   First-time container image pulls and dependency builds take 2–3 minutes.
2. **Handle the exit code:**

| Exit | Meaning | Action |
|---|---|---|
| 0 | Ready | Proceed to step 3 |
| 10 | Docker missing | Direct instructor to install Docker Desktop: https://www.docker.com/products/docker-desktop/ |
| 11 | Docker daemon not running | Ask instructor to start Docker Desktop and wait until the daemon is active |
| 12 | Port conflict (8000, 8001, or 8501) | Identify which process holds the port. Do not kill processes without instructor confirmation. |
| 13 | API or ChromaDB unhealthy | Check container logs (`docker compose logs api vector-db`), diagnose root cause, fix, and re-run. |
| 14 | Smoke test failed | Inspect failed assertions in `scripts/smoke.sh`, inspect API endpoints, and fix. |
| 15 | curl missing | Advise instructor to install curl. |
| 16 | OPENAI_API_KEY missing | Prompt instructor to copy `.env.example` to `.env` and set a valid `OPENAI_API_KEY`. |

3. **Verify the teaching environment:**
   - FastAPI Health: `curl -sf http://localhost:8000/health`
   - ChromaDB Heartbeat: `curl -sf http://localhost:8001/api/v1/heartbeat`
   - HR Corpus Seed Documents: `curl -sf http://localhost:8000/documents`
   - Streamlit Visual Explorer: `http://localhost:8501` (alias: `http://localhost:3000`)
   - FastAPI Interactive Docs: `http://localhost:8000/docs`
   - Course modules: verify `course/modules/01-transformers-and-attention.md` through `05-fine-tuning-and-evaluation.md` exist.
4. **Report readiness checklist:**
   - Present a concise table of endpoints, ports, container states, and quick-start instructions.
   - Mention helper scripts: `scripts/setup.sh --reset` (reseed documents) and `scripts/setup.sh --stop` (shut down stack).
5. **Prompt next step:**
   - Say: *"Ready to teach! Say 'teach module 1' when you are ready to begin."*

## Rules
- Idempotent: re-running on a healthy running stack is non-destructive and verifies status quickly.
- Do not expose or log real OpenAI API keys.
- Do not run `--reset` without explicit approval as it drops and reseeds the Chroma collection.
