# Instructor Guide — Agentic AI Engineering (Week 3 PM)

Agentic AI Engineering, taught with an AI co-pilot (Claude / Antigravity) and a shared **ClaimFlow AI** demo platform.

> AM Generative AI sessions are delivered by a separate instructor. This guide covers **PM sessions only**.

**In a hurry? See the [Class-day quick start](class-day-quickstart.md).**

---

## 1. How the PM course works

- **You teach; the agent co-pilots.** It keeps the class plan, runs demos, holds the answer key and tracks progress.
- **One example throughout:** ClaimFlow AI — a healthcare prior-authorization agent platform. Each PM class adds a new layer of agentic capability to the same running application.
- **Structure:** 5 PM modules (Mon–Fri), each split into *beats* (concept, demo, questions, exit check).

| # | PM Class | Topic | Demo script | Stack start |
|---|---|---|---|---|
| 1 | Monday PM | LangChain & LangGraph — State, Cycles, Checkpointing | `python examples/pm/01_langgraph_deep_dive.py` | `scripts/setup.sh` |
| 2 | Tuesday PM | Tool Calling & Structured Outputs — ReAct, Schemas, Parallel | `python examples/pm/02_react_tools_deep_dive.py` | `scripts/setup.sh` |
| 3 | Wednesday PM | MCP & Agent Memory — JSON-RPC, Tiers, TTL, Isolation | `python examples/pm/03_mcp_memory_deep_dive.py` | `scripts/setup.sh` |
| 4 | Thursday PM | Multi-Agent Workflows — Supervisor, Pipeline, Critic | `python examples/pm/04_multi_agent_deep_dive.py` | `scripts/setup.sh` |
| 5 | Friday PM | HITL, Guardrails & Evaluation — Approval gates, Red-team, RAGAS | `python examples/pm/05_hitl_evaluation_deep_dive.py` | `scripts/setup.sh` |

---

## 2. Before your first class (one time)

1. Install **Python 3.10+** and (optionally) **Docker Desktop**.
2. Clone this repository (`agentic-ai-course/`) and open it in Claude Code or Antigravity IDE, so the skills in `.claude/skills/` load. Start a **new session** after opening.
3. Say **"set up the agentic class"** (skill `setup-agentic-class`). It installs dependencies, starts the ClaimFlow API, and runs a 7-check smoke test.
4. Optionally set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` to demonstrate real LLM calls; all demos work offline without keys.

---

## 3. Running a class

Say **"teach class N"** (skill `teach-agentic-class`).

The agent will:
1. Confirm the ClaimFlow stack is healthy and offer to resume unfinished progress.
2. Show objectives, beats, estimated time, and today's ClaimFlow milestone.
3. Ask **"Is your screen shared?"** Answers are withheld until you ask.
4. Run each beat: *Concept* → *Live demo* → *Questions* → *Wait for you.*

**Your controls:**

| Say | Effect |
|---|---|
| `next` / `back` | Move between beats |
| `repeat` | Re-run the last demo |
| `skip` | Skip beat and log it |
| `answer [n]` | Reveal the answer |
| `more` | Another question or example |
| `status` | Progress and time |
| `take over` | You run the demo; agent waits |
| `break <fault>` | Inject a live fault |
| `fix` | Restore healthy baseline |
| `end` | Wrap up |

---

## 4. Class-day checklist
- [ ] Python 3.10+ environment with `pip install -r requirements.txt` done
- [ ] `scripts/setup.sh` (or `scripts/setup.ps1`) reports READY
- [ ] Today's `examples/pm/0N_*.py` runs cleanly
- [ ] `pytest tests/ -v` shows all tests PASSED
- [ ] Browser dashboard open at http://localhost:8000

---

## 5. Module beats at a glance

### Class 1 — LangChain & LangGraph (~90 min)
| Beat | Topic | Demo |
|---|---|---|
| 1.1 | LCEL linear chain vs StateGraph | Architecture comparison printout |
| 1.2 | TypedDict state schema + `Annotated` reducers | Live state construction |
| 1.3 | Nodes, edges, conditional routing | Graph compilation and visualization |
| 1.4 | Cyclic retry loop with bounded counter | End-to-end graph execution |
| 1.5 | Durable checkpoint with MemorySaver | Thread checkpoint read-back |
| 1.6 | Simulated crash & restart recovery | Re-instantiate graph + retrieve state |
| 1.7 | Escalation path when retries exhausted | Bounded retry → escalate node |

### Class 2 — Tool Calling & Structured Outputs (~90 min)
| Beat | Topic | Demo |
|---|---|---|
| 2.1 | LLM tool selection & OpenAI JSON schema | Schema printout |
| 2.2 | Pydantic input validation | Valid vs invalid schema rejection |
| 2.3 | ReAct Thought → Action → Observation loop | Full trace printout |
| 2.4 | Sequential vs parallel tool execution | Timing benchmark |
| 2.5 | Tool timeout & cache fallback | Fault injection + recovery |
| 2.6 | Structured output & schema coercion | Model vs raw string comparison |

### Class 3 — MCP & Agent Memory (~90 min)
| Beat | Topic | Demo |
|---|---|---|
| 3.1 | MCP `initialize` handshake frame | Raw JSON-RPC printout |
| 3.2 | `tools/list` discovery | Schema listing |
| 3.3 | `tools/call` invocation | Full request/response cycle |
| 3.4 | Stdio vs Streamable HTTP transport | Architecture comparison |
| 3.5 | Short-term working memory (session scratchpad) | Write + read back |
| 3.6 | Long-term episodic memory (cross-session) | Persist + retrieve after restart |
| 3.7 | TTL cache expiration | 100ms expiry demonstration |
| 3.8 | Memory poisoning defense | Injection attempt + block |
| 3.9 | Cross-tenant isolation | Unauthorized access attempt |

### Class 4 — Multi-Agent Workflows (~90 min)
| Beat | Topic | Demo |
|---|---|---|
| 4.1 | Orchestration patterns comparison | Supervisor, Pipeline, Critic diagram |
| 4.2 | Supervisor dynamic routing | Low / high / experimental routing |
| 4.3 | Pipeline execution (Triage → Verifier → Auditor) | End-to-end trace with tokens |
| 4.4 | Typed state contract handoffs | State schema printout |
| 4.5 | Writer-Reviewer (Critic) iteration | Two-turn revision loop |
| 4.6 | Single-agent vs multi-agent benchmark | Token / cost / latency comparison |

### Class 5 — HITL, Guardrails & Evaluation (~90 min)
| Beat | Topic | Demo |
|---|---|---|
| 5.1 | HITL gate: 4 actions (Approve, Reject, Edit, Escalate) | High-dollar claim pause |
| 5.2 | Checkpoint pause + resume | State recovery after human edit |
| 5.3 | Idempotency replay defense | SHA-256 duplicate block |
| 5.4 | Multi-layer guardrails (Input / Tool / Output) | Architecture walkthrough |
| 5.5 | Red-team attack suite (5 vectors) | Live attack + block trace |
| 5.6 | RAGAS metrics | Faithfulness, Relevance, Recall scoring |
| 5.7 | LLM-as-Judge bias calibration | Position / verbosity / self-pref bias |
| 5.8 | Capstone: full ClaimFlow end-to-end | Submit → Triage → Policy → HITL → Approve |

---

## 6. Live fault injection (Class 5 Capstone)

```bash
bash scripts/break.sh invalid-codes       # malformed CPT codes
bash scripts/break.sh ineligible-patient  # inactive coverage
bash scripts/break.sh high-dollar-hitl    # triggers HITL gate ($15k claim)
bash scripts/break.sh tool-failure        # audit tool timeout → degraded fallback
bash scripts/break.sh prompt-injection    # jailbreak payload → guardrail block
bash scripts/break.sh cross-tenant-leak   # unauthorized cross-tenant query
bash scripts/fix.sh                       # restore healthy baseline
```

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: claimflow` | Run from `agentic-ai-course/` root; ensure venv activated |
| Port 8000 in use | `lsof -i :8000` / `netstat -ano \| find "8000"` → kill the process |
| `langgraph` ImportError | `pip install -r requirements.txt` again |
| All tests FAIL | Ensure PYTHONPATH includes the course root or `conftest.py` is present |
| Mock LLM output boring | Set `OPENAI_API_KEY` for real responses; all logic works without it |
