# Student Guide — Agentic AI Engineering (Week 3 PM)

Welcome to Week 3 PM — **Agentic AI Engineering**. Over five afternoon sessions you will build **ClaimFlow AI**, a production-grade multi-agent healthcare prior-authorization platform.

> The AM Generative AI foundation sessions are delivered by a separate instructor and covered in separate materials.

---

## 1. Environment Setup

### Prerequisites
- Python 3.10+
- Terminal (`bash` on macOS/Linux; PowerShell or Git Bash on Windows)
- (Optional) Docker Desktop

### Quick setup
```bash
# 1. Clone your course workspace
git clone <repo-url> agentic-ai-course
cd agentic-ai-course

# 2. Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt

# 3. Start ClaimFlow API (keep this terminal open)
python -m uvicorn claimflow.api.main:app --port 8000 --reload

# 4. Run smoke test (second terminal)
bash scripts/smoke.sh          # Linux / macOS
powershell -File scripts/smoke.ps1  # Windows

# 5. Verify all tests pass
pytest tests/ -v
```

Open http://localhost:8000 to view the ClaimFlow AI dashboard.

---

## 2. ClaimFlow AI — What You Are Building

ClaimFlow AI is a healthcare prior-authorization agent that processes insurance claims through specialized agents:

```
Claim Submitted
     │
     ▼
 TriageAgent          ← validates patient eligibility and claim codes
     │
     ▼
 PolicyVerifierAgent  ← retrieves and interprets clinical coverage criteria via RAG
     │
     ▼
 ClaimsAuditorAgent   ← cross-checks fraud history and financial limits
     │
     ▼
 Human Review Gate    ← pauses for human approval on high-dollar or edge cases
     │
     ▼
 Decision Engine      ← emits Approved / Denied / Pended + audit trail
```

---

## 3. Five PM Class Milestones

| Class | Day | Topic | What You Add to ClaimFlow |
|---|---|---|---|
| **1** | Monday PM | LangChain & LangGraph | State graph with cyclic retry and durable checkpoint |
| **2** | Tuesday PM | Tool Calling & Structured Outputs | Tool registry, ReAct loop, parallel execution |
| **3** | Wednesday PM | MCP & Agent Memory | MCP server, working + episodic memory, TTL cache |
| **4** | Thursday PM | Multi-Agent Workflows | Supervisor routing, pipeline, Writer-Reviewer critic |
| **5** | Friday PM | HITL, Guardrails & Evaluation | Approval gates, guardrails, RAGAS evaluation |

---

## 4. Running the Daily PM Demonstrations

Each PM class has an independently executable demonstration. Run them from the `agentic-ai-course/` root:

```bash
# Class 1 — Monday PM
python examples/pm/01_langgraph_deep_dive.py

# Class 2 — Tuesday PM
python examples/pm/02_react_tools_deep_dive.py

# Class 3 — Wednesday PM
python examples/pm/03_mcp_memory_deep_dive.py

# Class 4 — Thursday PM
python examples/pm/04_multi_agent_deep_dive.py

# Class 5 — Friday PM
python examples/pm/05_hitl_evaluation_deep_dive.py
```

---

## 5. Testing Your Code

Run all automated tests anytime:

```bash
pytest tests/ -v
```

Run only the tests for today's PM class:

```bash
# Class 1
pytest tests/test_graph.py tests/test_pm_demonstrations.py::test_pm_day1_demo_execution -v

# Class 2
pytest tests/test_tools.py tests/test_pm_demonstrations.py::test_pm_day2_demo_execution -v

# Class 3
pytest tests/test_mcp_memory.py tests/test_pm_demonstrations.py::test_pm_day3_demo_execution -v

# Class 4
pytest tests/test_multi_agent.py tests/test_pm_demonstrations.py::test_pm_day4_demo_execution -v

# Class 5
pytest tests/test_hitl_guardrails.py tests/test_edge_cases_security.py tests/test_pm_demonstrations.py::test_pm_day5_demo_execution -v
```

All tests run offline with zero paid API credits.

---

## 6. Using a Real LLM

All demos work in offline mock mode. To use a real frontier model:

```bash
export CLAIMFLOW_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
# OR
export CLAIMFLOW_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...

python examples/pm/01_langgraph_deep_dive.py
```

---

## 7. ClaimFlow API Reference

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/v1/patients` | List synthetic patients |
| POST | `/v1/claims` | Submit a prior-auth claim |
| POST | `/v1/claims/{id}/review` | Submit human review decision |
| GET | `/v1/mcp/tools` | List MCP tools |
| POST | `/v1/mcp/call` | Invoke an MCP tool |

Swagger UI: http://localhost:8000/docs
