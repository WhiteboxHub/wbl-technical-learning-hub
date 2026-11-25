# Class 1 — LangChain & LangGraph: State, Cycles and Checkpointing

Teach-skill content file. Format described in `.claude/skills/teach-agentic-class/SKILL.md`.
Stack: ClaimFlow AI at `http://localhost:8000` (`scripts/setup.sh` must be READY).
Time: about 90 minutes with demos and questions.

## Objectives
By the end, students understand why linear chains fail on retries, can build a typed LangGraph state schema with reducer operators, construct cyclic workflows with bounded retries, and recover durable state after a simulated process restart.

## Stack requirements
- ClaimFlow API running: `curl -sf http://localhost:8000/health`
- LangGraph installed: `python -c "from langgraph.graph import StateGraph; print('OK')"`

---

### Beat 1.1 — The limitation of linear chains
- **Concept:**
  - LangChain LCEL is a Directed Acyclic Graph (DAG): A → B → C. No loops, no retry on failure.
  - When a node fails (e.g. eligibility API timeout), the whole chain fails — no way to cycle back.
  - LangGraph introduces a *stateful* graph with explicit cycles and conditional edges.
- **Demo (run: instructor):**
  ```bash
  python examples/pm/01_langgraph_deep_dive.py
  ```
  **Point out:** Section `--- 1. Architecture Comparison ---` prints the limitation of LCEL and the advantage of StateGraph.
- **Ask:**
  - Q: What is the fundamental structural limitation of a DAG for agentic workflows? — A: It cannot loop back; once a node fails there is no way to retry without re-running the whole pipeline.
  - Q: Name two real-world reasons an agent node might need to retry. — A: Transient API timeout, rate-limit 429, network glitch, database lock.
- **Done when:** students can articulate why DAGs cannot handle retries.

---

### Beat 1.2 — TypedDict state schema and `Annotated` reducers
- **Concept:**
  - LangGraph state is a `TypedDict`. Each key has a reducer that merges partial updates.
  - Default reducer: replace. `Annotated[List[str], operator.add]` appends without overwriting.
  - This is critical for append-only audit logs and distributed message accumulation.
- **Demo (run: agent):**
  ```bash
  python -c "
  import operator
  from typing import Annotated, TypedDict, List
  from langgraph.graph import StateGraph, END, START

  class DemoState(TypedDict):
      count: int
      log: Annotated[List[str], operator.add]

  def node_a(s):
      print('node_a sees log:', s['log'])
      return {'count': s['count'] + 1, 'log': ['step-a']}

  def node_b(s):
      print('node_b sees log:', s['log'])
      return {'count': s['count'] + 1, 'log': ['step-b']}

  g = StateGraph(DemoState)
  g.add_node('a', node_a)
  g.add_node('b', node_b)
  g.add_edge(START, 'a')
  g.add_edge('a', 'b')
  g.add_edge('b', END)
  app = g.compile()
  r = app.invoke({'count': 0, 'log': ['start']})
  print('Final log:', r['log'])
  "
  ```
  **Point out:** `log` accumulates across all nodes because of `operator.add`; `count` overwrites.
- **Ask:**
  - Q: What reducer would you use for a message list in a multi-agent chat? — A: `Annotated[List[Message], operator.add]`.
  - Q: Why is append-only important for a healthcare audit trail? — A: Regulatory immutability; you must never lose a prior step in the adjudication chain.
- **Done when:** students can write a TypedDict with at least one `Annotated` reducer.

---

### Beat 1.3 — Conditional routing and cyclic edges
- **Concept:**
  - `add_conditional_edges(source, routing_fn, {return_value: target_node})` enables branching.
  - A cycle is created by routing back to the same node (e.g. `"retry": "validation"`).
  - Bounded retry: the state tracks `attempts`; the router checks the counter.
- **Demo (run: instructor):** Point to `01_langgraph_deep_dive.py`, sections `route_validation` and `build_demo_graph`.
  **Point out:** The `attempts < 3` guard is what prevents an infinite loop.
- **Ask:**
  - Q: What prevents the cyclic graph from running forever? — A: The `attempts` counter in the state; the router redirects to `escalate` once the bound is reached.
  - Q: Where is the routing logic — inside a node or on an edge? — A: On a conditional edge, expressed as a pure Python function.
- **Done when:** students can draw the ClaimFlow retry graph on a whiteboard.

---

### Beat 1.4 — Executing the graph — live trace
- **Concept:** Walk through the actual output printed by the demo.
- **Demo (run: agent):**
  ```bash
  python examples/pm/01_langgraph_deep_dive.py
  ```
  **Point out:** Attempt 1 fails (transient timeout), Attempt 2 succeeds, audit log shows all five entries appended via `operator.add`.
- **Ask:**
  - Q: How many entries are in the audit log at the end, and why? — A: Five — one initial + one from intake + one per attempt + one from resolution.

---

### Beat 1.5 — Durable checkpointing with MemorySaver
- **Concept:**
  - `MemorySaver` stores the full graph state keyed by `thread_id` after every node execution.
  - If the process crashes, the same `thread_id` retrieves the last saved state.
  - In production: replace `MemorySaver` with `SqliteSaver` or a Postgres checkpointer.
- **Demo (run: agent):** Point to Section `4. Inspecting Durable Checkpoint`.
  **Point out:** `app.get_state(config)` returns `checkpoint_state.values` — the same state that was produced inside the graph.
- **Ask:**
  - Q: What two things does `MemorySaver` need to retrieve a checkpoint? — A: The compiled graph and the `thread_id` in the config.

---

### Beat 1.6 — Simulated crash and restart recovery
- **Demo (run: agent):** Point to Section `5. Simulating Process Crash & Restart Recovery`.
  **Point out:** A brand-new `StateGraph` instance instantiated after the "crash" retrieves the same thread from `MemorySaver` because the saver object persists in the same Python process (or in a persistent backend in production).
- **Ask:**
  - Q: What needs to change to make checkpointing survive a real server restart? — A: Use a persistent checkpointer backend: `SqliteSaver`, Redis, or Postgres.
- **Done when:** students understand that MemorySaver is in-process; production uses a persistent backend.

---

### Beat 1.7 — Escalation path when retries are exhausted
- **Demo (run: agent):** Point to Section `6. Edge Case: Bounded Retries Exceeded`.
  **Point out:** After 3 attempts the router returns `"escalate"` → `escalate_node` logs the event and ends the graph cleanly.
- **Ask:**
  - Q: Why is clean escalation better than an unhandled exception? — A: The claim is not silently dropped; it enters a human review queue with a full audit trail.

---

## Exercise
Build a two-node LangGraph workflow with a `ClaimState` TypedDict that:
1. Has an `audit_log: Annotated[List[str], operator.add]` field.
2. Simulates a transient failure on the first attempt.
3. Succeeds on the second attempt.
4. Prints the full audit log at the end.

Expected output includes at least `["start", "attempt 1 failed", "attempt 2 succeeded"]`.

## Done-check
- [ ] Students can explain why LCEL chains cannot retry.
- [ ] Students can write a TypedDict state with an `Annotated` list reducer.
- [ ] Students can add a conditional edge that cycles back to a node.
- [ ] Students can retrieve a MemorySaver checkpoint by thread ID.
- [ ] `pytest tests/test_graph.py -v` passes.

## Clean-up
No state to clean up. `MemorySaver` is in-process only.
