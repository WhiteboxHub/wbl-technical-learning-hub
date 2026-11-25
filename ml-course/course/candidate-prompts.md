# Week 2 PM — Candidate Evening Rhythm & Agent Prompts

Every evening after class (~2 hours):

| Step | Time | What to Do |
|---|---|---|
| **Tutor Agent** | 30 min | Rebuild today's story in your own words using the day's Story Anchor; fill every gap class left. |
| **Practice Agent** | 45 min | Complete today's hands-on work locally with saved evidence (files, terminal outputs, screenshots). |
| **Coding Agent** | 30 min | Build and review today's code; hints before solutions, always (`question -> hint -> outline -> code`). |
| **Quiz Agent** | 15 min | Closed-book quiz on today only; weak areas named, not hidden. |
| **Daily Report** | 5 min | Send the Daily Report block to your instructor the same evening. |

### Evening Plan Checklist (Every Day)
- [ ] Tutor session done — I can retell today's story without notes
- [ ] Practice work done, with evidence saved
- [ ] Code runs locally on my machine *(CoderPad has no candidate-facing entry point — every task is runnable locally)*
- [ ] Quiz taken; weak areas written into my Candidate State (`.candidate/state.md`)
- [ ] Candidate State updated and carried to the next agent
- [ ] Daily Report sent to the instructor

---

## Monday — ML Lifecycle + MLflow Experiment Tracking
- **Deeper understanding:** *An experiment you cannot reproduce is a rumour. MLflow is the lab notebook that turns rumours into engineering.*
- **Tutor Prompt:** `Tutor Agent: Today we covered ML Lifecycle + MLflow Experiment Tracking. Teach it back to me using the story anchor (The lab notebook: a scientist who cannot reproduce last Tuesday's result has an anecdote, not a result). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.`
- **Practice Prompt:** `Practice Agent: Give me hands-on practice for ML Lifecycle + MLflow Experiment Tracking (The ML lifecycle end to end: data, train, evaluate, register, deploy, monitor; Why experiments without tracking become archaeology; MLflow tracking: params, metrics, artifacts, runs). One task at a time, real-scenario based, increasing difficulty. Check my evidence after each task before giving the next. Do not do the task for me.`
- **Coding Prompt:** `Coding Agent: I am building today's work on ML Lifecycle + MLflow Experiment Tracking. Review my code in this order: does it run, is it correct, is it readable, is it production-shaped? Use your hint ladder - question, hint, outline, then code - and stop at the lowest rung that unblocks me.`
- **Quiz Prompt:** `Quiz Agent: Quiz me on ML Lifecycle + MLflow Experiment Tracking, one question at a time, no answers until the end. Score me per topic, name my weak areas, update my Candidate State, and close with the Daily Report block ready for me to send to my instructor.`

---

## Tuesday — DVC + Data and Pipeline Versioning
- **Deeper understanding:** *Code without its data is a recipe without the ingredients list from that day. DVC is how the ingredients get remembered.*
- **Tutor Prompt:** `Tutor Agent: Today we covered DVC + Data and Pipeline Versioning. Teach it back to me using the story anchor (The time machine for data: Git remembers the code, DVC remembers the world the code ran on). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.`
- **Practice Prompt:** `Practice Agent: Give me hands-on practice for DVC + Data and Pipeline Versioning (Why Git alone cannot version data; DVC remotes, .dvc files, checkout and pull; Pipelines as code: stages, dependencies, dvc repro). One task at a time, real-scenario based, increasing difficulty. Check my evidence after each task before giving the next. Do not do the task for me.`
- **Coding Prompt:** `Coding Agent: I am building today's work on DVC + Data and Pipeline Versioning. Review my code in this order: does it run, is it correct, is it readable, is it production-shaped? Use your hint ladder - question, hint, outline, then code - and stop at the lowest rung that unblocks me.`
- **Quiz Prompt:** `Quiz Agent: Quiz me on DVC + Data and Pipeline Versioning, one question at a time, no answers until the end. Score me per topic, name my weak areas, update my Candidate State, and close with the Daily Report block ready for me to send to my instructor.`

---

## Wednesday — Model Deployment: FastAPI + Docker
- **Deeper understanding:** *A model in a notebook helps nobody. Deployment is the moment ML becomes a product — with users, errors, and consequences.*
- **Tutor Prompt:** `Tutor Agent: Today we covered Model Deployment - FastAPI + Docker. Teach it back to me using the story anchor (The restaurant opens: the recipe leaves the test kitchen and has to survive paying customers). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.`
- **Practice Prompt:** `Practice Agent: Give me hands-on practice for Model Deployment - FastAPI + Docker (Serving patterns: REST API, batch, streaming - and choosing; FastAPI model service: schema, validation, error behaviour; Containerising the service with Week 1's Docker skills). One task at a time, real-scenario based, increasing difficulty. Check my evidence after each task before giving the next. Do not do the task for me.`
- **Coding Prompt:** `Coding Agent: I am building today's work on Model Deployment - FastAPI + Docker. Review my code in this order: does it run, is it correct, is it readable, is it production-shaped? Use your hint ladder - question, hint, outline, then code - and stop at the lowest rung that unblocks me.`
- **Quiz Prompt:** `Quiz Agent: Quiz me on Model Deployment - FastAPI + Docker, one question at a time, no answers until the end. Score me per topic, name my weak areas, update my Candidate State, and close with the Daily Report block ready for me to send to my instructor.`

---

## Thursday — Monitoring + Drift Detection
- **Deeper understanding:** *Deployment is not the finish line; it is the start of the model's exposure to a changing world. Monitoring is how you find out the world moved before your users do.*
- **Tutor Prompt:** `Tutor Agent: Today we covered Monitoring + Drift Detection. Teach it back to me using the story anchor (The lighthouse keeper: the model does not announce when the world has moved on). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.`
- **Practice Prompt:** `Practice Agent: Give me hands-on practice for Monitoring + Drift Detection (What to monitor: inputs, outputs, performance, latency, errors; Data drift vs concept drift - the world changes vs the meaning changes; Drift signals and statistics in plain terms). One task at a time, real-scenario based, increasing difficulty. Check my evidence after each task before giving the next. Do not do the task for me.`
- **Coding Prompt:** `Coding Agent: I am building today's work on Monitoring + Drift Detection. Review my code in this order: does it run, is it correct, is it readable, is it production-shaped? Use your hint ladder - question, hint, outline, then code - and stop at the lowest rung that unblocks me.`
- **Quiz Prompt:** `Quiz Agent: Quiz me on Monitoring + Drift Detection, one question at a time, no answers until the end. Score me per topic, name my weak areas, update my Candidate State, and close with the Daily Report block ready for me to send to my instructor.`

---

## Daily Report Template
```markdown
## Week 2 PM Daily Report — <Day>
- **Story retell:** <1-2 sentences in your own words>
- **Hands-on evidence:** <commands run / files created / test results>
- **Quiz score & weak areas:** <topics solid vs weak areas logged in Candidate State>
- **Blockers / questions for tomorrow:** <any open questions>
```
