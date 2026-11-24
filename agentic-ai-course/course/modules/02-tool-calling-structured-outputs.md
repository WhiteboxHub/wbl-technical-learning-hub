# Class 2 — Tool Calling & Structured Outputs: ReAct, Schemas, Parallel Execution

Teach-skill content file.
Stack: ClaimFlow AI at `http://localhost:8000`.
Time: about 90 minutes.

## Objectives
By the end, students understand how an LLM selects and invokes tools via JSON schemas, can implement the ReAct (Reason + Act) loop step-by-step, benchmark sequential vs parallel tool execution, and handle tool failure gracefully with a cache fallback.

## Stack requirements
- ClaimFlow API running: `curl -sf http://localhost:8000/health`
- Pydantic v2 installed: `python -c "import pydantic; print(pydantic.__version__)"`

---

### Beat 2.1 — How LLMs select tools
- **Concept:**
  - Modern LLMs receive a list of JSON Schema tool definitions alongside the prompt.
  - The model reasons about which tool to call and generates a structured `tool_call` object.
  - The host extracts the call, validates it against the schema, invokes the function, and feeds the result back.
- **Demo (run: agent):**
  ```bash
  python examples/pm/02_react_tools_deep_dive.py
  ```
  **Point out:** Section `--- 1. Tool Registry ---` prints the schema for each tool, including required parameters.
- **Ask:**
  - Q: Why is a JSON Schema (not just a docstring) used for tool definitions? — A: The LLM can be reliably instructed to output a structured object that is machine-parseable; a docstring alone gives no enforcement.
  - Q: Who validates the tool input before execution — the LLM or the host? — A: The host (via Pydantic here).

---

### Beat 2.2 — Pydantic input validation for tool calls
- **Concept:**
  - Pydantic models are used as the input contracts for each tool.
  - `model.model_fields` lists fields; `is_required()` identifies mandatory params.
  - If the LLM omits a required param, Pydantic raises `ValidationError` before the tool runs.
- **Demo (run: agent):** Point to Section `--- 3. Tool Schema Validation ---`.
  **Point out:** The malformed call (missing `patient_id`) raises a schema error that is caught cleanly — the agent does not crash.
- **Ask:**
  - Q: What happens when the LLM hallucinates a parameter name that is not in the schema? — A: Pydantic raises a `ValidationError`; the agent should catch it and ask the LLM to retry.

---

### Beat 2.3 — The ReAct loop: Thought → Action → Observation
- **Concept:**
  - ReAct is the dominant pattern for tool-using agents: *Reason about what to do, Act by calling a tool, Observe the result, Repeat.*
  - The loop terminates when the agent has enough information to generate a **Final Answer**.
  - Each step is logged for auditability.
- **Demo (run: agent):** Point to Section `--- 2. Step-by-Step ReAct Execution Trace ---`.
  **Point out:** `[Thought]`, `[Action]`, `[Observation]` lines make the reasoning explicit and debuggable.
- **Ask:**
  - Q: Why is making the Thought step explicit valuable for a healthcare system? — A: Clinical adjudication must be auditable; a Thought trace shows *why* the agent chose each action.
  - Q: When does the ReAct loop terminate? — A: When the agent has enough information to produce a Final Answer, or when a maximum step count is reached.

---

### Beat 2.4 — Sequential vs parallel tool execution benchmark
- **Concept:**
  - Tools that do not depend on each other can be dispatched concurrently via `ThreadPoolExecutor`.
  - `futures = [executor.submit(tool, args) for ...]` → `results = [f.result() for f in futures]`.
  - Benefit: near-halving of wall-clock time for two independent tools.
- **Demo (run: agent):** Point to Section `--- 4. Sequential vs Parallel Benchmark ---`.
  **Point out:** Parallel is ~45–50% faster than sequential because both 80ms tool calls overlap.
- **Ask:**
  - Q: When is parallel tool execution **unsafe**? — A: When one tool's output is needed as input to another (sequential dependency), or when tools share mutable state.

---

### Beat 2.5 — Timeout and cache fallback
- **Concept:**
  - Production agents must handle external service failures gracefully.
  - Pattern: attempt the live call; on `TimeoutError`, serve a stale cached result flagged for post-audit.
  - The agent degrades gracefully rather than failing the whole claim.
- **Demo (run: agent):** Point to Section `--- 5. Tool Timeout & Graceful Degradation ---`.
  **Point out:** `degraded_mode: True` in the response signals downstream agents that this result needs re-verification later.
- **Ask:**
  - Q: What is the risk of silently serving stale cached data? — A: The patient's eligibility may have changed; serving an old ACTIVE status could result in an erroneous approval.
  - Q: How do you mitigate that risk? — A: Flag the response as `degraded_mode`, log it, and schedule re-verification.

---

## Exercise
Extend the ReAct demo to add a third tool: `get_provider_reputation(provider_id: str)` that returns a fraud score. Wire it into the loop so the agent calls all three tools before producing its Final Answer.

Expected: a three-step Thought → Action → Observation trace ending with `[Final Answer]`.

## Done-check
- [ ] Students can describe the ReAct loop in their own words.
- [ ] Students can write a Pydantic tool input schema.
- [ ] Students understand when parallel execution is safe.
- [ ] Students can describe the timeout fallback pattern.
- [ ] `pytest tests/test_tools.py -v` passes.

## Clean-up
No persistent state. All tool calls are idempotent reads.
