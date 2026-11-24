# Class 4 — Multi-Agent Workflows: Supervisor, Pipeline and Critic

Teach-skill content file.
Stack: ClaimFlow AI at `http://localhost:8000`.
Time: about 90 minutes.

## Objectives
By the end, students can describe three multi-agent orchestration patterns, implement supervisor-based dynamic routing, trace a typed-state pipeline handoff, run a Writer-Reviewer revision loop, and quantify the token and latency trade-off between single-agent and multi-agent architectures.

## Stack requirements
- ClaimFlow API running: `curl -sf http://localhost:8000/health`
- Orchestrator importable: `python -c "from claimflow.core.orchestrator import get_claimflow_app; print('OK')"`

---

### Beat 4.1 — Multi-agent pattern overview
- **Concept:**
  - **Supervisor-Worker:** a central router analyses the task and delegates to specialist workers. Flexible; workers are independent.
  - **Sequential Pipeline:** a fixed assembly line (Triage → Verifier → Auditor). Predictable, easy to audit.
  - **Writer-Reviewer (Critic):** an iterative loop where a Drafter proposes an output and a Reviewer critiques it until quality gates are met.
- **Ask:**
  - Q: When is a Pipeline better than a Supervisor? — A: When every claim must go through every step in a fixed order (e.g. regulatory mandates).
  - Q: When is a Supervisor better? — A: When routing depends on claim complexity that is only known at runtime.

---

### Beat 4.2 — Supervisor dynamic routing
- **Demo (run: agent):**
  ```bash
  python examples/pm/04_multi_agent_deep_dive.py
  ```
  **Point out:** Section `--- 2. Supervisor Dynamic Routing ---`. Three claims get three different routes based on dollar amount and procedure code.
- **Ask:**
  - Q: What is the routing rule for experimental procedure codes? — A: Route to Medical Director Specialist (codes ending in `T` are experimental/investigational).
  - Q: What information must the Supervisor have to route correctly? — A: Claim amount, procedure code type, and potentially the patient's coverage tier.

---

### Beat 4.3 — Pipeline execution with typed state handoffs
- **Demo (run: agent):** Point to Section `--- 3. Multi-Agent Pipeline Execution ---`.
  **Point out:** Each agent logs its step, action, tokens consumed and cost. The trace shows *which agent did what* — essential for regulatory audit.
- **Ask:**
  - Q: Why does each agent receive a typed `ClaimState` rather than a raw dict? — A: Type safety prevents an agent from accidentally reading a field that does not exist or writing to the wrong key — "context blowout".
  - Q: What is the risk of passing a large unstructured context blob between agents? — A: Token waste, hallucinated field references, and difficulty debugging failures.

---

### Beat 4.4 — Writer-Reviewer (Critic) iteration loop
- **Demo (run: agent):** Point to Section `--- 4. Writer-Reviewer (Critic) Pattern ---`.
  **Point out:** Iteration 1: Drafter omits "physical therapy" → Auditor demands revision. Iteration 2: Drafter adds the evidence → Auditor approves.
- **Ask:**
  - Q: When should the Critic loop terminate automatically? — A: When the Reviewer's critique is "APPROVED", or after a maximum number of iterations to prevent infinite loops.
  - Q: What prevents the Critic loop from cycling forever? — A: A maximum iteration counter in the routing function (same pattern as bounded retry in Class 1).

---

### Beat 4.5 — Single-agent vs multi-agent benchmark
- **Demo (run: agent):** Point to Section `--- 5. Quantitative Benchmark ---`.
  **Point out:** Multi-agent uses more tokens (650 vs 450) and costs slightly more, but provides per-step audit trails, independent failure isolation, and specialized prompts.
- **Ask:**
  - Q: When does a single-agent monolith outperform multi-agent? — A: Simple tasks where the overhead of message passing and multiple LLM calls outweighs the benefit of specialisation.
  - Q: Why does regulatory healthcare adjudication favour multi-agent despite the extra token cost? — A: Each agent's decision and reasoning must be independently logged and auditable for CMS and HIPAA compliance.

---

## Exercise
Add a fourth specialist agent `FraudDetectionAgent` to the pipeline that checks the provider's reputation score from the memory store. If `fraud_rate > 0.3`, it should add a flag to the state before adjudication.

Expected: the execution trace shows four agent steps, with the fraud flag appearing in the state for high-risk providers.

## Done-check
- [ ] Students can name and contrast the three orchestration patterns.
- [ ] Students can explain the advantage of typed state handoffs over raw dicts.
- [ ] Students can implement a two-turn Writer-Reviewer loop with a termination condition.
- [ ] Students can explain the token / audit trade-off.
- [ ] `pytest tests/test_multi_agent.py -v` passes.

## Clean-up
No persistent state.
