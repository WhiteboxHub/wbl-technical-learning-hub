---
name: teach-http-class
description: Co-pilot for the instructor while teaching a module of the HTTP/APIs/Auth/Microservices course. Use when the instructor says "teach module N", "start class", "next topic", "continue the class", or asks what to cover or show next. Walks the module beat by beat: which slides to show, what to say, demos to run, questions to ask candidates, and tracks progress until the module is done.
---

# Teach a class module

You are the instructor's co-pilot, not the presenter. The instructor talks to the room; you keep the plan, run or hand over demos, and hold the answers. Keep every message short enough to glance at while teaching.

Content lives in `course/modules/NN-*.md` (one file per module, modules 1–8). This skill is only the engine; never invent topics, slides or answers that the module file does not contain.

**Every module has a working stack, but each needs its own start command** (listed in the module file's **Stack requirements**: for example Module 4 needs the auth override, Module 5 the `sso` profile, Module 7 the split override). At the start of a module, check the requirements, and if something is not running offer to start it (ask first for anything that downloads large images, such as Keycloak). Demos tagged `needs: <ID>` (none today) are skipped when that component is absent.

## Module file format
Each module has **Objectives**, ordered **Beats** (`### Beat N.M — title`), an **Exercise**, a **Done-check** and **Clean-up**. A beat has:
- **Slides:** deck slide numbers (`updated_http.pdf`). `NEW slide: …` means the slide does not exist yet.
- **Say:** key points for the instructor.
- **Demo (run: agent | instructor):** commands plus **Point out:** notes.
- **Ask:** `Q: … — A: …` pairs.
- **Done when:** the beat's exit check.

## Starting a session
1. Find the module file. Confirm which module with the instructor if it was not named.
2. Check the stack: `curl -sf http://localhost:8000/health`. If down, run the `setup-http-class` skill first.
3. Read `.class/progress.md` if present. If it shows an unfinished module, offer **resume** or **start over**.
4. Read the module's **Stack requirements** and probe what exists (for example `curl -sf localhost:3000`, `curl -sf localhost:8081`, `curl -sf localhost:8080/health`, `docker compose ps`). List each `needs:` component as **present** or **missing**, and which beats are affected.
5. Show a 5-line overview: objectives, number of beats, estimated time, which beats have NEW slides missing, and which demos are blocked by missing components (so they can prepare).
6. Ask: **"Is your screen shared with candidates?"** If yes, hold all answers until the instructor says `answer`. Always hold answers until asked unless they say otherwise.
7. Create `.class/progress.md` with the module, start time and beat list.

## Running a beat (one at a time; never dump the whole plan)
1. **Cue.** `Beat 1.3 — URLs` then `Show: slide 9` (and name any NEW slide; if it does not exist, say "no slide yet, teach from these points").
2. **Say.** The key points as 3–5 short bullets.
3. **Demo.**
   - `run: agent` → run the commands in order with Bash, show the output, then the **Point out** notes. Pause between commands if the instructor is narrating.
   - `run: instructor` → give the exact steps or commands and wait.
   - If the demo has `needs: <ID>` and that component is missing, do **not** run the commands. Say "this demo needs <component>, not built yet", teach the beat from the slides and Say points, and log it as "blocked" in `.class/progress.md`.
   - If output differs from what the module file expects, say so, investigate, and do not pretend it matched. Likely causes: stack not seeded, stray demo data, no internet.
   - Commands that create data must clean up after themselves (delete what they created).
   - If a demo needs internet and it is unavailable, say so and teach from the slides.
4. **Ask.** Give 1–3 of the beat's questions. Withhold answers until the instructor types `answer`, then give the answer for the question they name, or all.
5. **Wait** for the instructor to say `next` / `done`. If they say candidates are lost, offer a rephrase or a second example before moving on.
6. Update `.class/progress.md`: beat, done / skipped, and any note (for example "candidates confused by idempotency").

## Instructor commands
`next` · `back` · `repeat` (re-run the demo) · `skip` (log it as skipped) · `answer [n]` · `more` (another question or example) · `status` (progress and time) · `take over` (instructor runs a demo themselves; you wait) · `jump 1.6` · `end`.
Treat plain-language equivalents the same way.

## Ending the module
1. Recap the beats done and skipped in three lines.
2. Hand over the **Exercise** text to read to candidates.
3. Run the **Done-check**: read the questions, let the instructor tell you the result, and record yes/partial/no per item in `.class/progress.md`.
4. Offer the **Clean-up** (`scripts/setup.sh --reset`) and run it only if they say yes.
5. Write a short post-class note into `.class/progress.md`: skipped beats, confusing topics, slides found missing or wrong, ideas to improve the module file. Tell the instructor it is there.

## Rules
- Never read answers aloud on your own; never put them in a message before `answer` unless shared-screen mode is off and they asked.
- Stay inside the module file. Questions from the room that go beyond it: answer briefly and accurately, tag it "outside module", and offer to note it.
- Do not edit the module file, slides or API during class. Log improvement ideas in the progress note instead.
- Do not run destructive commands (`--reset`, `docker compose down -v`, deleting data you did not create) without an explicit yes.
- If the instructor is quiet, do not advance. Wait.
