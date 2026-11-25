# Instructor steps: how to start and take the class

Course: Agentic AI Engineering (Week 3 PM Sessions), taught with an AI co-pilot (Claude Code) and the ClaimFlow AI healthcare prior-authorization platform.
Project folder: `agentic-ai-course/`. Detailed guides: `agentic-ai-course/docs/instructor-guide.md` and `agentic-ai-course/docs/class-day-quickstart.md`.

## Before class

1. **Open the right folder.** In Claude Code, open `agentic-ai-course` (the folder that holds `.claude/skills/`) and start a **new session**. Skills only load at session start.
2. **Start the environment.** Either local Python:
   ```bash
   source .venv/bin/activate       # Linux/macOS (.venv\Scripts\activate on Windows)
   python -m uvicorn claimflow.api.main:app --port 8000 --reload
   ```
   Or via Docker Desktop: `docker compose up --build -d`
3. **Verify readiness.** Run the smoke test in a separate terminal:
   ```bash
   bash scripts/smoke.sh           # Linux/macOS
   powershell -File scripts/smoke.ps1  # Windows
   ```
4. **Open your presentation slides & dashboard.** Open the ClaimFlow UI at [http://localhost:8000](http://localhost:8000) on the screen you will share or demo from.

## Starting the class

1. Say **"set up the class"** (or `"get ready to teach"`). It checks Python/Docker, dependencies, starts ClaimFlow, verifies the 7 smoke endpoints, and ends with **READY**.
2. Say **"teach class N"** (e.g. `teach class 1` or `teach module 1`).
3. The agent checks stack requirements, shows an overview of the objectives, estimated time, and today's ClaimFlow milestone.
4. It asks: **"Is your screen shared with students?"** If yes, all answers to classroom questions remain hidden until you explicitly type `answer`.

## Start commands by PM class

| Class | Topic | Verification & Demo Command | Key Artifacts |
|---|---|---|---|
| **Class 1 (Mon)** | LangChain & LangGraph | `python examples/pm/01_langgraph_deep_dive.py` | StateGraph, reducers, cycles, checkpointer |
| **Class 2 (Tue)** | Tool Calling & Structured Outputs | `python examples/pm/02_react_tools_deep_dive.py` | ReAct loop, Pydantic schemas, parallel tools |
| **Class 3 (Wed)** | MCP & Agent Memory | `python examples/pm/03_mcp_memory_deep_dive.py` | JSON-RPC 2.0 MCP, episodic memory, vector RAG |
| **Class 4 (Thu)** | Multi-Agent Workflows | `python examples/pm/04_multi_agent_deep_dive.py` | Supervisor, pipeline, critic, token metrics |
| **Class 5 (Fri)** | HITL, Guardrails & Evaluation | `python examples/pm/05_hitl_evaluation_deep_dive.py` | HITL gates, injection defenses, RAGAS evals |

Run the complete test suite anytime: `pytest tests/ -v` (all 34 tests pass offline in deterministic mock mode).

## During class

The agent co-pilot works one beat at a time: it gives you the concept headline, key bullet points for the room, executes or hands over live code demos, and provides questions for students.

| You say | What happens |
|---|---|
| `next` / `back` | Move forward or backward between beats |
| `repeat` | Re-run the current beat's demo script or command |
| `skip` | Skip the current beat and log it in `.class/progress.md` |
| `answer [n]` | Reveal the hidden answer to classroom question n |
| `more` | Provide an additional real-world example or follow-up question |
| `status` | Display module progress, completed beats, and elapsed time |
| `take over` | You run the demo yourself; the agent pauses until you say `done` |
| `break <fault>` | Inject a live fault scenario during Class 5 capstone |
| `fix` | Restore healthy baseline after fault injection |
| `end` | Wrap up class and write `.class/progress.md` |

### Class 5 Capstone Fault Injections
To run live troubleshooting clinics during Class 5, inject faults one at a time:
- `break invalid-codes` — CPT/ICD-10 validation failure
- `break ineligible-patient` — Inactive policy denial
- `break high-dollar-hitl` — High-cost threshold triggers approval gate
- `break tool-failure` — Simulated audit tool timeout and fallback
- `break prompt-injection` — Jailbreak attempt intercepted by guardrail

Run `fix` (or `bash scripts/fix.sh` / `powershell -File scripts/fix.ps1`) to reset the baseline.

## At the end of each class

1. Say `end`. The agent recaps beats completed and skipped, provides the student hands-on exercise prompt, and runs the done-check.
2. It writes a session report to `.class/progress.md` logging student engagement, confusing topics, and timing notes.
3. Run `scripts/fix.sh` before the next session.

## If something goes wrong

| Problem | Do this |
|---|---|
| Port 8000 is in use | Run `lsof -i :8000` (macOS/Linux) or `netstat -ano \| findstr :8000` (Windows) and terminate the hanging process |
| Python package missing | Run `pip install -r requirements.txt` inside active virtual environment |
| Smoke test fails | Confirm uvicorn is running: `curl http://localhost:8000/health`; review terminal log |
| Skill not found in Claude | You started Claude Code from the parent directory; open `agentic-ai-course/` in a fresh session |
| Test claim data dirty | Run `bash scripts/fix.sh` (or `powershell -File scripts/fix.ps1`) to reset in-memory claims store |

## Students

Send students `agentic-ai-course/docs/student-guide.md`. 
Before class they say **"set up my environment"**; after class they say **"quiz me"** or **"help with the exercise"**.
