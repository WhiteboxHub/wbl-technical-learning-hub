# Weekend — Instructor Follow-Up, Self-Test & Exit Gate

## Weekend — Instructor Follow-Up (No Class)
There is **no class on Saturday or Sunday**, no demo/gate scheduled over the weekend, and **no submission deadline on the weekend itself**.

Over the weekend the instructor:
1. Reviews every candidate's **Daily Reports** and **Friday-evening Weekly Rollup**.
2. Verifies assignment and Fraud Detection stage completion (including any Friday overflow stages).
3. Notes batch-wide weak areas.
4. Sends each candidate a short follow-up note:
   - What is solid
   - The one re-do that matters
   - One thing to watch
5. Collects open questions to open Monday's class with.

Candidates may do optional self-paced catch-up with their agents (Tutor re-explains a weak topic, Practice sets extra problems, Quiz re-tests it).

---

## Candidate Self-Test — Worked Template Build: MLOps Fraud Detection System
Take this **closed book** on Friday evening or over the weekend before checking the answers below. Update your **Candidate State** (`.candidate/state.md`) with anything you miss.

1. What four things must be versioned for reproducibility?
2. DVC vs MLflow — who owns what?
3. Why validate inputs at the serving API?
4. Data drift vs concept drift — one example of each.
5. What makes an alert useful rather than noise?
6. Walk the ML lifecycle from data to monitoring.

---

## Self-Test Answers (Check Only After Finishing)
1. **Code, data, parameters, and environment.**
2. **DVC** versions data and pipelines; **MLflow** tracks experiments and the model registry.
3. Malformed input otherwise corrupts predictions silently; validation makes it a visible error.
4. **Data drift:** customer age mix shifts (input distribution changes). **Concept drift:** what "fraud" looks like changes as attackers adapt.
5. It fires on a condition someone will act on, at a rate a human can keep up with.
6. **Data -> Train -> Evaluate -> Register -> Deploy -> Monitor** — then loop on drift and retraining.

---

## Handoff to Week 3
Week 3 changes the raw material: **from tables to language**. Everything you proved here about tracking, serving, and monitoring returns in Weeks 4–5 as production AI engineering. Carry your Fraud Detection build and your Candidate State forward.
