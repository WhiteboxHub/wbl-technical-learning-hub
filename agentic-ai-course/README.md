# Agentic AI Engineering — Week 3 PM Course

> **PM Sessions only.** The AM Generative AI foundation sessions are delivered by a separate instructor and are outside this repository's scope.

Running example: **ClaimFlow AI** — a production-grade healthcare prior-authorization agent platform built progressively across all five PM classes.

## Guides & Documentation
- [Instructor Steps](instructor-steps.md) — Day-of-class step-by-step cheat sheet & voice controls
- [Course Table of Contents](docs/course-toc.md) — Comprehensive syllabus and topic breakdown
- [Class-day quick start](docs/class-day-quickstart.md) — 5-minute instructor checklist
- [Instructor Guide](docs/instructor-guide.md) — Setup, running a PM class with the agent, module plans, troubleshooting
- [Student Guide](docs/student-guide.md) — Environment setup, ClaimFlow architecture, daily exercises

## Start the stack
Requires Python 3.10+ (or Docker Desktop).

```bash
# Local Python:
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python -m uvicorn claimflow.api.main:app --port 8000 --reload

# Or Docker:
docker compose up --build -d

# Verify
bash scripts/smoke.sh      # bash
# PowerShell: powershell -File scripts/smoke.ps1
```

- **ClaimFlow API:** [http://localhost:8000](http://localhost:8000)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Dashboard:** [http://localhost:8000](http://localhost:8000)

Run the PM test suite:
```bash
pytest tests/ -v
```

Reset: `docker compose down -v && docker compose up --build -d`

## PM Class Modules

| # | PM Class | Topic | Demo Script | Tests |
|---|---|---|---|---|
| 1 | Monday PM | LangChain & LangGraph | `python examples/pm/01_langgraph_deep_dive.py` | `pytest tests/test_graph.py tests/test_pm_demonstrations.py::test_pm_day1_demo_execution -v` |
| 2 | Tuesday PM | Tool Calling & Structured Outputs | `python examples/pm/02_react_tools_deep_dive.py` | `pytest tests/test_tools.py tests/test_pm_demonstrations.py::test_pm_day2_demo_execution -v` |
| 3 | Wednesday PM | MCP & Agent Memory | `python examples/pm/03_mcp_memory_deep_dive.py` | `pytest tests/test_mcp_memory.py tests/test_pm_demonstrations.py::test_pm_day3_demo_execution -v` |
| 4 | Thursday PM | Multi-Agent Workflows | `python examples/pm/04_multi_agent_deep_dive.py` | `pytest tests/test_multi_agent.py tests/test_pm_demonstrations.py::test_pm_day4_demo_execution -v` |
| 5 | Friday PM | HITL, Guardrails & Evaluation | `python examples/pm/05_hitl_evaluation_deep_dive.py` | `pytest tests/test_hitl_guardrails.py tests/test_edge_cases_security.py tests/test_pm_demonstrations.py::test_pm_day5_demo_execution -v` |

Run all five demos end-to-end: `pytest tests/ -v`

## Layout
```
agentic-ai-course/
├── claimflow/           # ClaimFlow AI application (the progressive teaching platform)
│   ├── api/             # FastAPI REST + SSE server
│   ├── agents/          # Multi-agent orchestration patterns
│   ├── core/            # Models, state graph, LLM provider, orchestrator
│   ├── data/            # Synthetic healthcare knowledge base
│   ├── guardrails/      # Security, PII, injection defenses
│   ├── mcp/             # Model Context Protocol server (JSON-RPC 2.0)
│   ├── memory/          # Short-term / long-term / episodic memory
│   └── tools/           # Healthcare tools + vector RAG store
├── examples/pm/         # Five independently executable PM demonstrations
│   ├── 01_langgraph_deep_dive.py
│   ├── 02_react_tools_deep_dive.py
│   ├── 03_mcp_memory_deep_dive.py
│   ├── 04_multi_agent_deep_dive.py
│   └── 05_hitl_evaluation_deep_dive.py
├── tests/               # 34 Automated PM tests (unit + integration + demo verification)
├── course/modules/      # PM module files (beat-by-beat instructor scripts)
├── course/stack-backlog.md # Component architecture & verification ledger
├── docs/                # Instructor guide, student guide, quickstart, course-toc
├── postman/             # Postman collection for the ClaimFlow API
├── scripts/             # setup.sh/ps1, smoke.sh/ps1, break.sh/ps1, fix.sh/ps1
├── web/                 # ClaimFlow AI browser dashboard
├── .claude/skills/      # setup-agentic-class, setup-candidate, teach-agentic-class, practice-agentic
├── Dockerfile
├── docker-compose.yml
├── instructor-steps.md
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```

## Notes
- **Zero paid API credits required.** All five PM classes run offline in deterministic mock mode.
- Set `CLAIMFLOW_LLM_PROVIDER=openai` + `OPENAI_API_KEY=…` to use real frontier models.
- `scripts/break.sh <fault>` injects live faults for the capstone debugging clinic.
- `scripts/fix.sh` restores a healthy baseline.
- The `http-course/` and all other courses in this repository are **unmodified**.
