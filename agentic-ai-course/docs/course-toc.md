# Week 3 PM — Agentic AI Engineering: Table of Contents

5 PM classes. No topic dropped. Running application: **ClaimFlow AI** (healthcare prior-authorization agentic platform). Environment: Python + FastAPI + LangGraph, local or Docker.

| # | PM Class | Core Topics | Demo Script |
|---|---|---|---|
| 1 | LangChain & LangGraph | State, reducers, nodes, edges, conditional routing, cycles, checkpointing | `examples/pm/01_langgraph_deep_dive.py` |
| 2 | Tool Calling & Structured Outputs | ReAct loop, JSON schema, Pydantic validation, parallel tools, fallback | `examples/pm/02_react_tools_deep_dive.py` |
| 3 | MCP & Agent Memory | JSON-RPC 2.0, stdio/HTTP transport, short/long-term memory, TTL, isolation | `examples/pm/03_mcp_memory_deep_dive.py` |
| 4 | Multi-Agent Workflows | Supervisor-worker, sequential pipeline, writer-reviewer, handoffs, cost analysis | `examples/pm/04_multi_agent_deep_dive.py` |
| 5 | HITL, Guardrails & Evaluation | Approve/reject/edit/escalate, idempotency, guardrail layers, red teaming, RAGAS | `examples/pm/05_hitl_evaluation_deep_dive.py` |

---

## PM Class 1 — LangChain & LangGraph
**Module:** [`course/modules/01-langgraph-state-cycles.md`](../course/modules/01-langgraph-state-cycles.md)

1. **LangChain LCEL vs LangGraph:** Linear chains vs stateful graphs; DAG limitations vs cyclic capability.
2. **TypedDict State Schema:** Typed state definitions; field reducers with `Annotated[List[str], operator.add]`.
3. **Nodes and Edges:** `add_node`, `add_edge`, `set_entry_point`; `START` and `END` sentinels.
4. **Conditional Routing:** `add_conditional_edges`; routing functions returning string keys.
5. **Cycles and Bounded Retries:** Cyclic edges for retry loops; max-step guards to prevent infinite loops.
6. **Durable Checkpointing:** `MemorySaver`; `thread_id` config; `get_state()` inspection.
7. **Crash & Restart Recovery:** Reattaching a new graph instance to an existing checkpoint.

**ClaimFlow Application Build:** Add `StateGraph` backbone — `triage → verify_policy → audit_claim → decision` nodes with conditional routing.

Labs: Build a retry-with-escalation graph; simulate crash and recover state; trace the full audit log.

---

## PM Class 2 — Tool Calling & Structured Outputs
**Module:** [`course/modules/02-tool-calling-structured-outputs.md`](../course/modules/02-tool-calling-structured-outputs.md)

1. **Tool Definition:** OpenAI-compatible JSON schema generation from Pydantic models.
2. **Pydantic Input Validation:** `BaseModel`, `Field`, `ValidationError`; required vs optional parameters.
3. **ReAct Loop:** Thought → Action → Observation cycle; step-by-step reasoning trace with intermediate telemetry.
4. **Tool Selection:** LLM-driven tool dispatch; registry lookup; unknown-tool error handling.
5. **Sequential vs Parallel Execution:** `ThreadPoolExecutor` fan-out; latency benchmark comparison.
6. **Timeout & Fallback:** `TimeoutError` handling; graceful degradation to cached local data.
7. **Structured Outputs:** Schema-validated JSON responses; parsing and error recovery.

**ClaimFlow Application Build:** Wire `check_patient_eligibility` and `validate_medical_codes` tools into the triage agent with schema validation.

Labs: Define a new tool with Pydantic schema; trace a full ReAct loop; run parallel tool calls and measure speedup.

---

## PM Class 3 — MCP & Agent Memory
**Module:** [`course/modules/03-mcp-and-memory.md`](../course/modules/03-mcp-and-memory.md)

1. **Model Context Protocol (MCP):** JSON-RPC 2.0 lifecycle — `initialize`, `tools/list`, `tools/call`, `resources/list`.
2. **Transport Layers:** Stdio (child-process pipe) vs Streamable HTTP (SSE + POST); trade-offs for local vs distributed.
3. **Tool and Resource Discovery:** Dynamic capability negotiation; schema introspection at runtime.
4. **Short-Term Working Memory:** Session scratchpad; observation accumulation within a single claim.
5. **Long-Term Episodic Memory:** Cross-session persistence; prior authorization history; provider compliance records.
6. **Vector Memory:** Semantic embedding; cosine similarity search; tenant-scoped RAG retrieval.
7. **TTL Cache Expiration:** Time-to-live on eligibility tokens; cache miss handling; stale data prevention.
8. **Memory Security:** Poisoning defense; forbidden signature detection; cross-tenant isolation enforcement.

**ClaimFlow Application Build:** Expose `check_eligibility`, `validate_codes`, `search_policies` tools over MCP server; integrate `AgentMemoryStore` into the auditor agent.

Labs: Send a full MCP JSON-RPC exchange; store and retrieve episodic memory; trigger TTL expiration; attempt cross-tenant access.

---

## PM Class 4 — Multi-Agent Workflows
**Module:** [`course/modules/04-multi-agent-workflows.md`](../course/modules/04-multi-agent-workflows.md)

1. **Why Multi-Agent:** Specialization, failure isolation, parallel throughput, regulatory auditability.
2. **Supervisor-Worker Pattern:** Central router analyzes complexity; dispatches to specialist crews.
3. **Sequential Pipeline Pattern:** Fixed stage assembly — Triage → Policy Verifier → Auditor → Decision Engine.
4. **Writer-Reviewer (Critic) Pattern:** Drafter proposes; Auditor critiques; iterative revision loop.
5. **Typed State Handoffs:** `ClaimState` as shared contract; preventing context blowout between agents.
6. **Shared State vs Message Passing:** When to use a common state object vs explicit inter-agent messages.
7. **Agent Handoff Mechanics:** `return state` as the inter-agent contract; trace entry per agent.
8. **Cost & Latency Benchmark:** Single-agent monolith vs multi-agent crew — tokens, latency, failure isolation.

**ClaimFlow Application Build:** `TriageAgent`, `PolicyVerifierAgent`, `ClaimsAuditorAgent`, `DecisionEngine` operating as a full supervisor-worker pipeline.

Labs: Run the full multi-agent pipeline; inject a fault in one agent and observe isolation; compare token costs.

---

## PM Class 5 — HITL, Guardrails & Agent Evaluation
**Module:** [`course/modules/05-hitl-guardrails-evaluation.md`](../course/modules/05-hitl-guardrails-evaluation.md)

1. **HITL Full Lifecycle:** Pause at approval gate → 4 reviewer actions (Approve, Reject, Edit & Approve, Escalate) → Resume from checkpoint.
2. **Durable Approval Persistence:** State survives process restart; reviewer picks up exactly where it paused.
3. **Idempotency & Replay Defense:** SHA-256 signature registry; duplicate submission blocking; bypass prevention.
4. **Input Guardrails:** PII redaction (SSN, phone, email); prompt injection detection and hard rejection.
5. **Tool Guardrails:** Financial approval caps; negative-amount prevention; tool-call schema enforcement.
6. **Output Guardrails:** Mandatory policy citation validation; hallucinated code rejection.
7. **Red Teaming:** 5 adversarial attack vectors — prompt injection, PII exfiltration, bypass, fee tampering, hallucinated codes.
8. **Agent Evaluation — RAGAS:** Faithfulness, Answer Relevance, Context Recall, Harm Avoidance metrics.
9. **LLM-as-Judge:** Bias calibration — position bias, verbosity bias, self-preference mitigation.
10. **Execution Tracing:** Per-step `AuditTraceEntry`; token and cost accounting; full claim lineage.

**ClaimFlow Application Build:** Complete end-to-end — HITL gate on high-dollar claims, all three guardrail layers active, RAGAS evaluation suite.

Labs: Submit a high-dollar claim and exercise all 4 HITL actions; run the red team suite; compute RAGAS scores on sample outputs.

---

## Every PM Class Ships With

| Item | Location |
|---|---|
| Beat-by-beat instructor script | `course/modules/0N-*.md` |
| Standalone executable demo | `examples/pm/0N_*_deep_dive.py` |
| Automated test coverage | `tests/test_*.py` |
| Instructor guide | `docs/instructor-guide.md` |
| Student guide | `docs/student-guide.md` |
| Class day quickstart | `docs/class-day-quickstart.md` |
| Setup skill (instructor) | `.claude/skills/setup-agentic-class/` |
| Setup skill (candidate) | `.claude/skills/setup-candidate/` |
| Teaching co-pilot skill | `.claude/skills/teach-agentic-class/` |
| Practice assistant skill | `.claude/skills/practice-agentic/` |

## Open Points
- Real LLM integration (OpenAI / Anthropic / Gemini) tested separately when API keys are available; all classes run fully in mock mode without keys.
- Docker Compose setup mirrors local Python setup; both paths verified on Windows, macOS and Linux.
- Day 5 capstone is the complete ClaimFlow AI pipeline running all five days' components end-to-end.
