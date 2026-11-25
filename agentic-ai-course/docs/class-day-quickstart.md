# Class-Day Quick Start — Agentic AI Engineering PM (Week 3)

**Goal:** have ClaimFlow AI running and the first PM demo verified before students arrive (5 minutes).

```bash
# 1. Enter the course directory
cd agentic-ai-course

# 2. Activate virtual environment (or use Docker — see README)
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows

# 3. Start ClaimFlow API (foreground; open a second terminal for demos)
python -m uvicorn claimflow.api.main:app --port 8000 --reload

# 4. Smoke test (second terminal)
bash scripts/smoke.sh           # Linux / macOS
powershell -File scripts/smoke.ps1  # Windows

# 5. Verify today's PM demo executes cleanly
python examples/pm/01_langgraph_deep_dive.py   # Monday
python examples/pm/02_react_tools_deep_dive.py # Tuesday
python examples/pm/03_mcp_memory_deep_dive.py  # Wednesday
python examples/pm/04_multi_agent_deep_dive.py # Thursday
python examples/pm/05_hitl_evaluation_deep_dive.py  # Friday

# 6. Run PM test suite
pytest tests/ -v
```

## Checklist
- [ ] Python 3.10+ and `pip install -r requirements.txt` done
- [ ] `uvicorn` serving ClaimFlow API on port 8000
- [ ] `smoke.sh` reports ALL CHECKS PASSED (7 checks)
- [ ] Today's `examples/pm/0N_*.py` demo runs without error
- [ ] `pytest tests/ -v` shows all 34+ tests PASSED
- [ ] Browser opens http://localhost:8000 (ClaimFlow dashboard)

## Controls during class (say to the agent)
| Say | Effect |
|---|---|
| `teach class 1` | Start Monday PM (LangGraph) |
| `teach class 2` | Start Tuesday PM (Tools) |
| `teach class 3` | Start Wednesday PM (MCP & Memory) |
| `teach class 4` | Start Thursday PM (Multi-Agent) |
| `teach class 5` | Start Friday PM (HITL & Evaluation) |
| `next` / `back` | Move between beats |
| `answer [n]` | Reveal answer to question n |
| `break <fault>` | Inject a live fault scenario |
| `fix` | Restore healthy baseline |
| `status` | Progress and time used |
| `end` | Wrap up and write progress note |

## Fault injection for capstone (Friday)
```bash
bash scripts/break.sh invalid-codes       # malformed CPT codes
bash scripts/break.sh ineligible-patient  # inactive coverage
bash scripts/break.sh high-dollar-hitl    # triggers HITL gate
bash scripts/break.sh tool-failure        # audit tool timeout
bash scripts/break.sh prompt-injection    # jailbreak attempt
bash scripts/break.sh cross-tenant-leak   # multi-tenant isolation test
bash scripts/fix.sh                       # restore baseline
```
