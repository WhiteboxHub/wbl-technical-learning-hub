# Quick Copy-Paste Prompts for ChatGPT & Any AI Coding Agent

Paste the GitHub URL to `wbl-technical-learning-hub/mysql-course` (or upload the `mysql-course` folder/zip) into **ChatGPT**, **Claude**, **Gemini**, **Antigravity**, or **Cursor**, then copy one of the prompts below.

---

## 1. Full Guided Step-by-Step Study Mode (Recommended!)
```text
I am studying the Whitebox Learning `mysql-course` repository (`wbl-technical-learning-hub/mysql-course`).
Read `AGENTS.md`, `docs/learning-plan.md`, `docs/schema-reference.md`, `course/modules/`, and `course/self-study/` first.

Guide me step by step through Module [1 / 2 / 3 / 4] (or `course/self-study/` after Module 4):
1. Teach ONE Beat at a time using the module's Story Anchor, a plain-language explanation, one `training_db` example, and the Candidate Takeaway.
2. After each Beat, ask me 1 check question (or ask me to explain it back in my own words) and WAIT for my answer before moving on.
3. Once I finish the Beats, walk me through `db/labs/` ONE task at a time (ask me to predict row counts first; use hints before solutions).
4. At the end, quiz me with 8 questions ONE at a time (no answers until the end), then score me, name my weak areas, and output my DAILY REPORT and UPDATED CANDIDATE STATE.

Let's begin! Confirm my starting module and teach Beat 1.
```

---

## 2. "Help Me Explain What My Instructor Covered in the 2-Hour Class"
```text
Read `AGENTS.md`, `docs/schema-reference.md`, and `course/modules/`.
Today in our 2-hour class my instructor covered Module [1 / 2 / 3 / 4] (or specific topics: [paste]).
Teach these topics back to me one Beat at a time using the Story Anchor and Candidate Takeaway.
After each Beat, ask me to explain the concept back in my own words and correct any gap before moving on.
Do not solve my lab queries for me.
```

---

## 3. SQL Query Review & Debugging (Hint-First Mode)
```text
Read `AGENTS.md`, `docs/schema-reference.md`, and `prompts/03-coding-agent.md`.
Act as my MySQL SQL Coach. Lab task: [paste task]
My SQL query:
```sql
[paste your SQL]
```
Review it in order (syntax/execution -> NULLs/duplicates/index SARGability -> readability -> 1-2 improvements). Use the 4-Rung Hint Ladder before giving solutions.
```

---

## 4. End-of-Module Quiz & Evaluation
```text
Read `AGENTS.md`, `prompts/04-quiz-agent.md`, and `course/modules/[file].md` (or `course/self-study/[file].md`).
Quiz me on Module [1 / 2 / 3 / 4 / Self-Study 1 / Self-Study 2] with 8 questions, ONE question at a time.
Mix conceptual, "explain in your own words", senior scenario, and "predict row count / EXPLAIN" questions.
Do NOT reveal any answers or hints while the quiz is running.
After question 8, give my score, explain missed questions, list weak areas in priority order, and output my DAILY REPORT and UPDATED CANDIDATE STATE.
```
