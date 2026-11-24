# Class 5 — HITL, Guardrails and Agent Evaluation: Approval, Red-Teaming, RAGAS

Teach-skill content file.
Stack: ClaimFlow AI at `http://localhost:8000`.
Time: about 90–100 minutes (includes capstone).

## Objectives
By the end, students can implement the four HITL actions (Approve, Reject, Edit, Escalate), prevent duplicate execution with idempotency, build multi-layer guardrails (Input / Tool / Output), execute an adversarial red-team suite, compute RAGAS evaluation metrics, and calibrate LLM-as-Judge bias.

## Stack requirements
- ClaimFlow API running: `curl -sf http://localhost:8000/health`
- Guardrails importable: `python -c "from claimflow.guardrails.security import GuardrailsManager; print('OK')"`

---

### Beat 5.1 — Why Human-in-the-Loop is not optional in healthcare
- **Concept:**
  - CMS and HIPAA regulations mandate a human reviewer for high-dollar, experimental, or edge-case prior-authorizations.
  - The agent pauses at a gate; the state is persisted; a human reviews asynchronously; the agent resumes.
  - Four possible human actions: Approve (as-is), Reject (with documented reason), Edit-and-Approve (adjust amount or codes), Escalate (to external peer-review board).
- **Ask:**
  - Q: What is the difference between Reject and Escalate? — A: Reject is a final denial with documented clinical reason. Escalate is a referral to a medical board for further independent review.

---

### Beat 5.2 — HITL pause, edit and resume
- **Demo (run: agent):**
  ```bash
  python examples/pm/05_hitl_evaluation_deep_dive.py
  ```
  **Point out:** Section `--- 1. Human-in-the-Loop (HITL) 4-Action Lifecycle ---`. The $16,500 claim triggers `pending_human_approval`. The human edits the amount to $14,500 and resumes. Status becomes `approved` with `MODIFIED_AND_APPROVED_BY_HUMAN`.
- **Ask:**
  - Q: Why must the HITL pause state be persisted (checkpointed)? — A: The human reviewer may not act for hours or days; the process cannot block waiting in memory.
  - Q: What happens to claims currently in `pending_human_approval` if the system restarts? — A: With durable checkpointing they survive and resume where they left off.

---

### Beat 5.3 — Idempotency and replay prevention
- **Demo (run: agent):** Point to Section `--- 2. Idempotency ---`.
  **Point out:** A SHA-256 signature of `claim_id + action + token` is stored; re-submitting the same approval is blocked immediately.
- **Ask:**
  - Q: What attack does idempotency prevent? — A: A malicious actor replaying a valid approval token to authorize multiple claims.
  - Q: What must be unique in the idempotency key? — A: The combination of claim ID, action type, and reviewer token — none alone is sufficient.

---

### Beat 5.4 — Multi-layer guardrails architecture
- **Concept:**
  - Layer 1 (Input): sanitize PII (SSN, phone), detect prompt injection before the input reaches the agent.
  - Layer 2 (Tool): enforce financial limits; prevent negative amounts; validate provider IDs against registry.
  - Layer 3 (Output): ensure the final decision includes a mandatory policy citation; block unsafe clinical recommendations.
- **Ask:**
  - Q: Why is filtering only at the output layer insufficient? — A: By then the agent may have already called a tool or generated a decision based on the malicious input — the damage is done.

---

### Beat 5.5 — Red-team adversarial attack suite
- **Demo (run: agent):** Point to Section `--- 4. Adversarial Red Teaming Attack Suite ---`.
  **Point out:** Five attack types are executed: Direct Prompt Injection, PII Exfiltration, Approval Bypass, Fee Schedule Tampering, Hallucinated Code Injection. Each is blocked by a different layer.
- **Ask:**
  - Q: Which attack does Guardrail Layer 1 (Input) block? — A: PII exfiltration and prompt injection.
  - Q: Which attack does Guardrail Layer 2 (Tool) block? — A: Fee schedule tampering (the amount exceeds the allowed ceiling).
  - Q: What would you need to block "Hallucinated Code Injection" (fake CPT code)? — A: A code validation tool (ICD-10/CPT registry lookup) in Layer 2.

---

### Beat 5.6 — RAGAS evaluation metrics
- **Concept:**
  - RAGAS measures four aspects of a RAG-based agent: Faithfulness (claims grounded in retrieved docs), Answer Relevance (response addresses the question), Context Recall (all required docs were retrieved), Harm Avoidance (no unsafe outputs).
  - Scores are normalized 0–1; production gate: all metrics ≥ target.
- **Demo (run: agent):** Point to Section `--- 5. Agent Evaluation ---`.
  **Point out:** The ClaimFlow system scores 0.98, 0.95, 1.00, 1.00 — all above target.
- **Ask:**
  - Q: What does Faithfulness = 0.98 mean? — A: 98% of the agent's statements can be directly attributed to retrieved policy documents; 2% are potentially hallucinated.
  - Q: Why is Context Recall = 1.00 especially critical for prior-authorization? — A: If a mandatory clinical criterion is not retrieved, it cannot be applied — leading to an erroneous approval or denial.

---

### Beat 5.7 — LLM-as-Judge bias calibration
- **Concept:**
  - LLM judges suffer from Position Bias (favouring the first option), Verbosity Bias (favouring longer answers), and Self-Preference Bias (favouring outputs from the same model family).
  - Calibration: swap order, normalise by length, cross-validate with a different model family.
- **Ask:**
  - Q: Why does using a GPT-4 judge to evaluate GPT-4 outputs introduce bias? — A: Self-preference — the judge tends to rate outputs from its own model family higher.

---

### Beat 5.8 — Capstone: full ClaimFlow end-to-end
- **Demo (run: instructor):**
  - Use the fault injection scripts to simulate a real class exercise:
  ```bash
  bash scripts/break.sh prompt-injection
  python examples/pm/05_hitl_evaluation_deep_dive.py
  bash scripts/fix.sh
  ```
  Walk students through the full flow: a claim is submitted → Triage → Policy → HITL gate triggered → human edit → Approved.
- **Ask:**
  - Q: What single change would make this system production-ready that we have not built? — A: A real persistent checkpointer (Postgres), authentication on the HTTP API, and a production LLM provider.

---

## Exercise
Write a custom guardrail that blocks any claim where `requested_amount > 50000` before it reaches the HITL gate, returning a rejection with the reason `"Exceeds single-claim ceiling; refer to committee review"`.

## Done-check
- [ ] Students can implement the four HITL actions.
- [ ] Students can explain the role of idempotency in preventing replay attacks.
- [ ] Students can design a three-layer guardrail stack.
- [ ] Students can run the red-team suite and explain which layer blocks each attack.
- [ ] Students can interpret a RAGAS score table.
- [ ] `pytest tests/test_hitl_guardrails.py tests/test_edge_cases_security.py -v` passes.
- [ ] Full end-to-end ClaimFlow capstone runs without error.

## Clean-up
Run `bash scripts/fix.sh` to restore a clean baseline after any fault injections.
