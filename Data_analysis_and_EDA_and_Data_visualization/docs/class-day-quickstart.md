# Class Day Quickstart: Data Analysis (5-Minute Launch Guide)

Welcome Instructor! Follow this concise checklist to launch your live teaching session in under 5 minutes.

---

## 1. Pre-Flight Verification (T-Minus 5 Minutes)

Run the automated setup and smoke test suite to guarantee environment readiness:
```bash
# From repository root
bash scripts/setup.sh
bash scripts/smoke.sh
```
Both commands must exit with `[ALL TESTS PASSED]`.

---

## 2. Launch Your AI Teaching Co-Pilot

Depending on your coding agent environment:

### Option A: Google Antigravity / Gemini CLI
Simply ask:
> *"I am starting class now. Activate data-analysis-skill in Instructor Mode and guide me through the opening hook."*

### Option B: Claude Code
Run:
```bash
claude
# Prompt: Read instructor-steps.md and act as my live co-pilot for Beat 1.
```

### Option C: Cursor / Windsurf / Codex
Open `instructor-steps.md` and type in chat:
> *"Follow instructor-steps.md and give me the opening hook and Beat 1 cues."*

---

## 3. During-Class Controller Commands

Speak or type these quick commands to your agent during lecture:
- `next` — Move to the next beat.
- `answer` — Reveal the model answer to the in-class question.
- `repeat` — Re-explain the current concept with an alternate analogy.
- `more` — Deep dive into memory layouts or internal C implementations.
- `status` — View which beats are completed vs pending in `.class/progress.md`.

---

## 4. Emergency Fallback Quick Reference

If candidate environments encounter issues:
- **Missing packages:** `pip install -r requirements.txt`
- **Plots not rendering:** Figures are saved automatically to `demos/output/*.png`. Direct candidates to view the image files directly.
- **Corrupted files / reset:** Run `bash scripts/reset.sh`.

