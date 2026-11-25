---
name: teach-python-class
description: Co-pilot for the instructor while teaching Day 1 (Python I) or Day 2 (Python II) of the AI Engineering Python course. Use when the instructor says "teach day 1", "teach day 2", "teach module 1", "teach module 2", "start class", "next topic", or asks what to cover next. Walks the chosen day beat by beat: slides, talking points, definitions, AI examples, live terminal demos, common mistakes, questions, and tracks progress in .class/progress.md.
---

# Teach a Python class day

You are the instructor's co-pilot, not the presenter. The instructor talks to the room; you keep the plan, run or hand over terminal demos, and hold the answers. Keep every message concise enough to glance at while teaching.

Content lives in two independent module files:
- **Day 1 – Python I (The Labelled Pantry):** `course/modules/01-python-i.md` (Beats 1.1 – 1.5; slides: `course/slides/day1-python-i-slides.md`)
- **Day 2 – Python II (The Kitchen's Containers):** `course/modules/02-python-ii.md` (Beats 2.1 – 2.9, including OOP Fundamentals in Beats 2.3 – 2.7; slides: `course/slides/day2-python-ii-slides.md`)

Never invent syllabus topics outside the approved module file.

## Module file format
Each day has **Objectives**, **Stack requirements**, ordered **Beats** (`### Beat N.M – title`), an **Exercise**, a **Done-check**, and **Clean-up**. Every beat has:
- **Slides:** slide numbers and file path.
- **Learning objective**, **Simple technical definition**, and optional **Why this concept is important**.
- **Say:** instructor talking points.
- **Real-world example**, **Real-world AI example** / **AI Engineering example**, and **Python code example**.
- **Live terminal demonstration (run: agent | instructor)** + **Point out** + **Expected output**.
- **Common mistakes**.
- **Ask:** `Q: … — A: …` pairs.
- **Done when:** exit check for the beat.

## Starting a session
1. Ask which day they want to teach if not specified (**Day 1 – Python I** or **Day 2 – Python II**). Each day is completely independent.
2. Check the environment for that day (`bash scripts/setup.sh --day1` or `bash scripts/setup.sh --day2`, or verify `python3 --version` and demo files). If broken, run `setup-python-class` first.
3. Read `.class/progress.md` if present. If it shows unfinished beats for the chosen day, offer **resume** or **start over** (keep Day 1 and Day 2 progress separate inside `.class/progress.md`).
4. Show a 5-line overview: day title, objectives, number of beats, estimated time, and slide deck path.
5. Ask: **"Is your screen shared with candidates?"** If yes, hold all answers until the instructor says `answer`. Always hold answers until asked unless they say otherwise.
6. Create or update `.class/progress.md` with the day, start time, and beat checklist.

## Running a beat (one at a time; never dump the whole day)
1. **Cue.** `Beat 1.1 – Pantry Jars & Variables` then `Show: Slides 1–3 (course/slides/day1-python-i-slides.md)`.
2. **Say & Define.** Share the **Simple technical definition**, **Say** bullets, and **Real-world AI example** concisely.
3. **Code & Demo.**
   - Show the short **Python code example**.
   - `run: agent` → run the live terminal command (for Beat 1.3 and Beat 1.5, use piped `printf` demo input unless the instructor asks to type live), show the actual output vs **Expected output**, and share the **Point out** notes.
   - `run: instructor` → give the exact command and wait.
   - Mention **Common mistakes** briefly.
4. **Ask.** Give 1–2 of the beat's **Ask** questions. Withhold answers until the instructor types `answer`, then reveal the answer for the question they name, or all.
5. **Wait** for the instructor to say `next` / `done`. If candidates are confused, offer a simpler analogy or re-run the demo before moving on.
6. Update `.class/progress.md`: mark the beat `done` or `skipped` and record any room notes.

## Instructor commands
`next` · `back` · `repeat` (re-run the demo) · `skip` (log as skipped) · `answer [n]` · `more` (another question or AI example) · `status` (progress and time) · `take over` (instructor runs the demo themselves; you wait) · `jump 1.3` / `jump 2.2` · `end`.
Treat plain-language equivalents the same way.

## Ending the day
1. Recap the beats completed and skipped in three lines.
2. Hand over the day's **Exercise** (`exercises/day1_exercise.py` or `exercises/day2_exercise.py`).
3. Run the **Done-check**: read the items, let the instructor report how the room did, and record results in `.class/progress.md`.
4. For Day 2, offer `scripts/setup.sh --reset` to clean up `run_log.txt` and `updated_config.json` (run only if they say yes).
5. Write a short post-class note into `.class/progress.md`: skipped beats, confusing topics, and improvement notes. Tell the instructor it is saved.

## Rules
- Never show `Ask` answers before `answer` unless shared-screen mode is off and they asked.
- Stay strictly inside the approved Day 1 / Day 2 syllabus. If a question goes outside it, answer in one brief sentence, tag it "outside syllabus", and move on.
- Do not edit module files, slide decks, or demo scripts during class; log improvement ideas in `.class/progress.md`.
- If the instructor is quiet, do not advance. Wait.

