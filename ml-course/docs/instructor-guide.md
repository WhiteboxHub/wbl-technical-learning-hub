# Instructor Guide — Week 2 PM Production ML

Whitebox Learning — Agentic AI Engineering.
Each class runs as a **~3-hour block** (scalable as needed), **demo-first and concept-second**, built around a single **Story Anchor** per day and converging on Friday's **Fraud Detection System** template build.

**Quick start:** [Class-Day Quick Start](class-day-quickstart.md) · **Syllabus:** [Course TOC](course-toc.md).

---

## 1. Fixed Daily Cadence (Instructor Order)
Every day (`course/modules/01..05*.md`) follows the exact same order:
1. **Story Anchor** — open with it, return at every topic shift, close with it.
2. **Topics List** — 5 topics per day (Mon–Thu).
3. **The Class (Intro 15m -> Topics + Break -> Conclusion 15m)**:
   - *Intro:* Hook with anchor, state destination in 1 sentence, show end result first, name 3 questions.
   - *Topics:* Show demo first, then explain why it works.
   - *Conclusion:* 1-minute retelling, 3 things that survive the night, Exit Check out loud, 1-sentence hook for tomorrow.
4. **What the Candidate Must Know** — 3 concrete outcomes.
5. **Slides & Prompts (`5A` Material, `5B` Explanation Guide, `5C` Local Setup, `5D` Demo Programs)**.
6. **Real Scenarios**, **Exit Check with Answers**, and **Tutor Agent Prompt**.

## 2. Friday & Weekend Structure
- **Friday:** Worked Template Build (**MLOps Fraud Detection System**) across AM + PM sessions (`DVC -> features -> Logistic Regression -> MLflow -> FastAPI -> CI/CD -> monitoring & drift`), checkpointed at each stage against the guide.
  - **Overflow rule:** Any stage not finished in class on Friday becomes candidate self-work over the weekend; the instructor checks it in the weekend follow-up, and it is finished on Monday if needed.
  - **Exit Gate (Demonstrable Outcomes — no invented numeric pass thresholds):**
    1. Tracked MLflow experiment + registered model.
    2. DVC-versioned dataset + reproducible `dvc repro` pipeline.
    3. Model served from a Docker container behind FastAPI.
    4. Monitoring view detecting live-injected drift.
- **Weekend (No Class):** Instructor reviews Daily Reports & Friday Weekly Rollup, sends short follow-up notes (what is solid, 1 re-do, 1 thing to watch), and collects open questions for Monday.

## 3. Troubleshooting
| Issue | Fix |
|---|---|
| Port `5000` busy on macOS | Turn off AirPlay Receiver in System Settings, or change MLflow port mapping in `docker-compose.yml` to `5001:5000` |
| Windows `python3` opens Store | Use `python` (not `python3`) in PowerShell, or `py -3` |
| `dvc` command not found | Activate `.venv` or run inside `docker compose exec fraud-api ...` |
| Drift demo still shows old alerts | Run `bash scripts/fix.sh` (or `powershell -File scripts/fix.ps1`) |
