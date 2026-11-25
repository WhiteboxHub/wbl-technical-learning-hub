# Class-Day Quick Start (Instructor, 5 Minutes)

Quick-reference checklist for launching and leading a Week 3 AM class.

---

## 1. Open the folder in a NEW Claude Code session
Open `wbl-technical-learning-hub/genai-course`, then launch a **new session** in Claude Code. Skills are registered only upon session start.

## 2. Check `.env` and start Docker Desktop
Ensure Docker Desktop is open and green, and `.env` contains your `OPENAI_API_KEY`. Then say:
> **"set up the class"**

Wait for the **READY** output. The script boots:
- **FastAPI API** on `http://localhost:8000`
- **ChromaDB Vector DB** on `http://localhost:8001`
- **Streamlit UI** on `http://localhost:3000`
- Runs the 10-check smoke test and pre-seeds the 5 HR documents.

## 3. Open your slides and browser tabs
- Presenter Screen: Slides or talking bullets from `course/modules/NN-*.md`.
- Browser Tab 1: Streamlit UI at `http://localhost:3000`
- Browser Tab 2: Swagger UI at `http://localhost:8000/docs`

## 4. Begin Teaching
Say:
> **"teach module 1"** (or `teach module 2`, `teach module 3`, etc.)

The teaching co-pilot will verify stack readiness, ask if your screen is shared with students (to conceal answers), and deliver the lesson beat by beat.

### Quick Commands During Class
| Command | What happens |
|---|---|
| `next` / `done` | Advance to the next beat |
| `repeat` | Re-run the current demo |
| `skip` | Log beat as skipped and move ahead |
| `answer` | Reveal the answer key to the check question |
| `more` | Provide an additional example or question |
| `status` | View elapsed time and beats progress |
| `take over` | You lead the live demo; agent pauses |
| `jump N.M` | Navigate to specific beat (e.g. `jump 3.2`) |
| `end` | Conclude module with exercise and Done-check |

## 5. Troubleshooting Cheat Sheet
| Issue | Resolution |
|---|---|
| API shows "missing key" | Check `.env` has `OPENAI_API_KEY=sk-...` without quotes, then restart `docker compose restart api` |
| ChromaDB returns 0 documents | Run `scripts/setup.sh --reset` to clear vector volume and re-seed HR policies |
| Streamlit page won't load | Check `docker compose ps` to ensure the `ui` container is healthy |
| Port conflict | Stop conflicting services on ports 3000, 8000, or 8001 |
| Reset everything after class | Run `scripts/fix.sh` or `scripts/setup.sh --stop` |
