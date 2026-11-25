# Implementation Summary — Agentic AI Engineering (ClaimFlow AI)

This document provides a comprehensive overview of the architecture, components, teaching modules, and developer tooling implemented in the `agentic-ai-course/` repository.

---

## 1. Executive Summary

- **Course:** Week 3 PM — Agentic AI Engineering
- **Focus:** Practical, production-grade autonomous agent systems
- **Running Platform:** **ClaimFlow AI** — an enterprise healthcare prior-authorization platform built progressively across 5 PM classes.
- **Key Design Philosophy:** 
  - **Offline-first & zero cost:** Runs 100% locally with deterministic mock LLM execution; no paid API keys required for classroom delivery.
  - **Frontier model ready:** Seamlessly connects to real LLMs (OpenAI, Anthropic, Gemini) via environment variables.
  - **Strict isolation:** Completely contained within `agentic-ai-course/` with zero impact on other repository courses.

---

## 2. ClaimFlow AI Platform Architecture

ClaimFlow AI automates complex clinical prior-authorization workflows using autonomous multi-agent collaboration, structured tool calling, dynamic memory, and safety guardrails.

```
                    ┌────────────────────────────┐
                    │   Client / Web Dashboard   │
                    │      (FastAPI + SSE)       │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │    LangGraph StateGraph    │
                    │   (Cyclic State Machine)   │
                    └─────────────┬──────────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
┌──────────────┐          ┌──────────────┐          ┌───────────────────┐
│ Triage Agent │          │Policy Verifier│         │  Claims Auditor   │
│ (ReAct Loop) │          │ (Vector RAG) │          │  (Memory & Rules) │
└──────┬───────┘          └──────┬───────┘          └─────────┬─────────┘
       │                         │                            │
       └─────────────────────────┼────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │      Decision Engine       │
                    └─────────────┬──────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       [ Auto-Approval / Denial ]     [ HITL Human Review Gate ]
                                      (Paused in Checkpointer)
```

### Core Components Implemented

| Component | File Path | Implementation Details |
|---|---|---|
| **LangGraph Engine** | `claimflow/core/graph.py` | Stateful graph with `triage`, `verify_policy`, `audit_claim`, and `decision` nodes. Implements conditional edges, retry cycles with bounded step limits, and durable `MemorySaver` checkpointing. |
| **Tool Calling & ReAct** | `claimflow/tools/healthcare_tools.py` | Pydantic v2 validated tool definitions, OpenAI-compatible JSON schema generation, `check_patient_eligibility`, `validate_medical_codes`, parallel executor with latency benchmarking, and timeout fallbacks. |
| **Model Context Protocol** | `claimflow/mcp/server.py` | Native JSON-RPC 2.0 MCP server supporting `initialize`, `tools/list`, `tools/call`, and `resources/list` protocols over stdio and HTTP transports. |
| **Multi-Tier Memory** | `claimflow/memory/agent_memory.py` | Session working memory (scratchpad), episodic long-term memory across claims, TTL-based cache expiration, semantic vector store (cosine similarity), and cross-tenant memory isolation. |
| **Multi-Agent Systems** | `claimflow/agents/multi_agent.py` | Specialist agent crews implementing Supervisor-Worker, Sequential Pipeline, and Writer-Reviewer (Critic) patterns with typed `ClaimState` handoffs and token cost tracking. |
| **HITL Review Gates** | `claimflow/core/orchestrator.py` | Human-in-the-Loop approval checkpoints for high-dollar claims (>$10,000) or low confidence (<0.75). Supports `approve`, `reject`, `edit`, and `escalate` decisions. |
| **Security Guardrails** | `claimflow/guardrails/security.py` | Prompt injection detection, jailbreak pattern matching, HIPAA PII redactor (SSN, MRN, phone, email, patient names), and immutable audit trail logging. |
| **REST & SSE API** | `claimflow/api/main.py` | FastAPI server exposing endpoints for claim submission, claim state retrieval, HITL review resolution, MCP tool execution, and static dashboard hosting. |
| **Browser Dashboard** | `web/index.html` | Interactive single-page UI for submitting claims, inspecting real-time agent execution traces, and resolving pending HITL review requests. |

---

## 3. PM Course Curriculum & Modules

The course is organized into 5 afternoon modules (`course/modules/`), each containing clear objectives, beat-by-beat lecture talking points, live demos, and student exercises:

1. **Module 01 — LangChain & LangGraph (`01-langgraph-state-cycles.md`)**
   - LCEL vs LangGraph stateful cyclic graphs
   - `TypedDict` state schema and field reducers (`Annotated[List[str], operator.add]`)
   - Nodes, edges, conditional routing, and bounded cyclic retries
   - Durable checkpointing with `MemorySaver` and crash recovery

2. **Module 02 — Tool Calling & Structured Outputs (`02-tool-calling-structured-outputs.md`)**
   - Pydantic schema validation and JSON schema emission
   - ReAct (Thought → Action → Observation) loops
   - Dynamic tool selection and unknown tool error handling
   - Sequential vs parallel tool execution and timeout fallbacks

3. **Module 03 — MCP & Agent Memory (`03-mcp-and-memory.md`)**
   - Model Context Protocol (MCP) JSON-RPC 2.0 specification
   - Transport protocols: Stdio vs Streamable HTTP
   - Short-term working memory vs episodic long-term memory
   - Vector RAG semantic search, TTL cache expiration, and tenant isolation

4. **Module 04 — Multi-Agent Workflows (`04-multi-agent-workflows.md`)**
   - Why multi-agent: specialization, failure isolation, token economics
   - Orchestration patterns: Supervisor-Worker, Sequential Pipeline, Writer-Reviewer
   - Typed state contracts (`ClaimState`) and inter-agent handoffs
   - Cost and latency benchmarking: single monolith agent vs multi-agent crew

5. **Module 05 — HITL, Guardrails & Evaluation (`05-hitl-guardrails-evaluation.md`)**
   - Human-in-the-Loop review actions (`approve`, `reject`, `edit`, `escalate`)
   - Checkpoint persistence and workflow resumption
   - Security defenses: prompt injection, jailbreaks, PII masking
   - Evaluation frameworks: ground truth scoring, red teaming, and RAGAS metrics

---

## 4. Demonstrations, Tests & Verification

### Executable Demonstrations (`examples/pm/`)
Five independently runnable Python scripts providing terminal-based deep dives for each PM class:
- `examples/pm/01_langgraph_deep_dive.py`
- `examples/pm/02_react_tools_deep_dive.py`
- `examples/pm/03_mcp_memory_deep_dive.py`
- `examples/pm/04_multi_agent_deep_dive.py`
- `examples/pm/05_hitl_evaluation_deep_dive.py`

### Automated Test Suite (`tests/`)
**34 automated pytest tests** covering 100% of the platform:
- `tests/test_graph.py` — LangGraph state transitions, conditional edges, retry limits, checkpoints
- `tests/test_tools.py` — Tool validation, schema generation, parallel tool executor speedup
- `tests/test_mcp_memory.py` — JSON-RPC 2.0 MCP calls, memory persistence, TTL expiration, vector RAG
- `tests/test_multi_agent.py` — Supervisor-worker crew, pipeline execution, writer-reviewer loop
- `tests/test_hitl_guardrails.py` — HITL approval gates, state resumption, PII masking
- `tests/test_edge_cases_security.py` — Prompt injection defense, jailbreak detection, tenant isolation
- `tests/test_api.py` — FastAPI REST endpoints, claim submissions, HITL reviews, MCP tools
- `tests/test_pm_demonstrations.py` — End-to-end execution of all 5 PM class demonstration scripts

Run the full suite:
```bash
pytest tests/ -v
# 34 passed in ~30s
```

---

## 5. Developer & Instructor Tooling

| Tool / File | Purpose |
|---|---|
| **`instructor-steps.md`** | Day-of-class quick reference cheat sheet with voice controls, daily start matrix, and troubleshooting table. |
| **`postman/claimflow.postman_collection.json`** | Comprehensive Postman collection covering health, claims, HITL reviews, and MCP tools. |
| **`course/stack-backlog.md`** | Architecture component ledger detailing built features and verification checks. |
| **`pytest.ini`** | Explicit pytest configuration with test discovery paths and warning filters. |
| **`scripts/setup.sh` / `.ps1`** | Automated prerequisite checks, virtual environment setup, and dependency installation. |
| **`scripts/smoke.sh` / `.ps1`** | 7-point automated health check verifying all REST endpoints and agent execution. |
| **`scripts/break.sh` / `.ps1`** | Classroom fault injector simulating 5 production failure modes for Capstone debugging. |
| **`scripts/fix.sh` / `.ps1`** | Rapid baseline restorer resetting in-memory claim data and restoring healthy state. |
| **`Dockerfile` & `docker-compose.yml`** | Containerized deployment configuration for local or cloud environments. |
| **`.claude/skills/`** | 4 Claude Code AI skills: `teach-agentic-class`, `practice-agentic`, `setup-agentic-class`, `setup-candidate`. |

---

## 6. How to Run the Environment

```bash
# 1. Navigate to the course folder
cd agentic-ai-course

# 2. Setup environment
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 3. Start the ClaimFlow API & Dashboard
python -m uvicorn claimflow.api.main:app --port 8000 --reload

# 4. Run Smoke Test
bash scripts/smoke.sh           # macOS / Linux
powershell -File scripts/smoke.ps1  # Windows

# 5. Open Web UI
# Navigate to: http://localhost:8000
```
