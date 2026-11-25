# Instructor Steps: Week 2 Day 1 AM (Statistics & Probability for ML)

This document is the instructor's run sheet for teaching **Week 2 Day 1 Morning (AM): Statistics & Probability for ML**.

---

## 1. Pre-Class Setup (10 minutes before class)

1. Open your terminal in the repository root:
   ```bash
   cd /path/to/repo
   ```
2. Run the automated setup and verification script:
   ```bash
   scripts/setup.sh
   ```
   Wait for **READY**. This checks Python 3.10+, installs dependencies (`numpy`), verifies datasets (`data/`), and runs the smoke test.
3. Open your presentation slides:
   - Topic: *Statistics & Probability for ML*
   - Slides: WBL Week 2 AM Slide Deck
4. Launch your AI Co-pilot:
   - If using **Claude Code**: type `claude` in terminal, then say `"teach stats"`.
   - If using **Antigravity / Gemini CLI**: say `"teach stats"`.
   - If using **Cursor**: open Composer/Chat with `@course/modules/01-statistics-and-probability.md` and say `"teach module 1"`.
   - If using **Codex / Grok**: use the system prompt in `docs/agent-prompts.md`.

---

## 2. Starting the Session

1. The co-pilot greets you, reads `.class/progress.md` (or offers to start fresh), and presents the 5-line class overview.
2. The co-pilot will ask:
   > **"Is your screen shared with candidates?"**
   - Answer **yes** if candidates can see your AI output; the co-pilot will withhold answers until you explicitly type `answer`.
   - Answer **no** if you are viewing on a private second monitor.
3. Type `start` to begin Beat 1.1.

---

## 3. Running Beats (1.1 through 1.7)

For each beat, the co-pilot will present:
- **Cue:** Beat title and slide references.
- **Say:** 3–4 bullet talking points anchored to *the weather forecaster who is never certain, only honest about the odds*.
- **Demo:** Runnable code command and key points to emphasize.
- **Ask:** Check question to pose to the room.

### Instructor In-Class Control Commands
| Command | Effect |
|---|---|
| `next` | Advances to the next beat and logs progress in `.class/progress.md` |
| `back` | Returns to the previous beat |
| `repeat` | Re-executes or redisplays the current beat demo |
| `answer` | Reveals the hidden answer and explanation for the check question |
| `more` | Generates an alternate check question if candidates struggled |
| `skip` | Marks the current beat skipped and moves forward |
| `jump 1.M` | Jumps directly to Beat 1.M |
| `status` | Shows completed beats, current time elapsed, and remaining topics |
| `end` | Ends the teaching session and displays the exit recap |

---

## 4. Morning Lesson Plan Schedule

| Time | Beat | Title | Demo / Activity |
|---|---|---|---|
| 09:00 - 09:20 | Beat 1.1 | The Weather Forecaster & Uncertainty | Concept introduction & mental model |
| 09:20 - 09:50 | Beat 1.2 | Reading Shapes of Data | `python3 demos/demo1_distributions.py --samples 500` |
| 09:50 - 10:20 | Beat 1.3 | Spread, Variance & Why Mean Lies | `python3 demos/demo1_distributions.py --outlier 500.0` |
| 10:20 - 10:30 | **Break** | 10-Minute Coffee Break | Reset / informal Q&A |
| 10:30 - 11:10 | Beat 1.4 | Conditional Probability & Bayes | `python3 demos/demo2_bayes_calculator.py` |
| 11:10 - 11:35 | Beat 1.5 | Sampling Bias: Size Doesn't Fix Bias | `python3 demos/demo3_sampling_bias.py` (Part 1) |
| 11:35 - 11:50 | Beat 1.6 | Signal vs Noise in A/B Testing | `python3 demos/demo3_sampling_bias.py` (Part 2) |
| 11:50 - 12:00 | Beat 1.7 | Candidate Hands-on Exercise & Exit Check | Exercise handover & Done-check review |

---

## 5. Post-Class Handover to Candidates

1. Hand candidates the independent practice exercise:
   - **Bayes Calculator Drill:** Modify `demo2_bayes_calculator.py` with custom prevalence/FPR rates and explain the shift in posterior probability.
   - **Sampling Bias Audit:** Inspect `data/weather_forecaster_survey.csv` and identify selection vs random sampling error.
2. Instruct candidates to interact with the practice coach skill:
   - Say: `"quiz me on stats"` or `"practice stats"`
3. Candidates log their outcomes in `candidate-state.md`.

---

## 6. Troubleshooting Common In-Class Issues

| Issue | Resolution |
|---|---|
| `python3 not found` | Ensure Python 3.10+ is installed and in `$PATH` |
| Demo plot doesn't pop up | Demos print clean ASCII tables and diagnostics by default when GUI backend is headless |
| Candidate confused by Bayes base rate | Use the natural frequencies 10,000-person grid from Demo 2: $90 \text{ true positives} / (90 + 891) \approx 9.17\%$ |
| Reset progress tracking | Run `bash scripts/reset.sh` |
