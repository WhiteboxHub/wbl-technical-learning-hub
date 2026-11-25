# Class-Day Quick Start: Week 2 Day 1 AM
## Statistics & Probability for ML

Get ready to teach in 5 minutes.

- **Session:** Week 2 Day 1 Morning (AM)
- **Topic:** Statistics & Probability for ML
- **Story Anchor:** *The weather forecaster who is never certain, only honest about the odds*
- **Module File:** `course/modules/01-statistics-and-probability.md`
- **Total Duration:** 3 hours (7 beats, 3 runnable demos)

---

## 1. Environment Verification (T-minus 5 minutes)

In terminal, execute:
```bash
scripts/setup.sh
```

Wait for **READY**. It checks:
- Python 3.10+
- NumPy availability
- Starter datasets in `data/`
- Clean execution of all 3 morning demos via `scripts/smoke.sh`

---

## 2. Slides Setup

Open your slide presentation:
- **Deck:** Week 2 AM — Statistics & Probability for ML
- **Key Concepts:** Distributions, Skew, Outliers, Mean vs Median, Bayes' Theorem, Base Rates, Selection Bias, Signal vs Noise

---

## 3. Co-Pilot Launch

Choose your coding agent platform:
- **Claude Code CLI:** Run `claude`, then say:
  > **"teach stats"** or **"teach module 1"**
- **Antigravity / Gemini CLI:** Run in workspace and say:
  > **"teach stats"**
- **Cursor IDE:** Open chat with `@course/modules/01-statistics-and-probability.md` and type:
  > **"teach module 1 beat by beat"**
- **OpenAI Codex / Grok / ChatGPT:** Paste the co-pilot prompt from `docs/agent-prompts.md`.

---

## 4. Teaching Rhythm

For each beat:
1. **Cue:** Co-pilot shows the beat title and slide number.
2. **Say:** Speak the 3–4 concise bullet points anchored to the weather forecaster.
3. **Demo:** Run the demo script (or have co-pilot run it).
4. **Ask:** Pose the check question to the candidates.
5. Withhold the answer until you type `answer`.
6. Type `next` to advance.

---

## 5. Demos Cheat Sheet

| Demo | Command | Core Lesson |
|---|---|---|
| **Demo 1: Distributions & Spread** | `python3 demos/demo1_distributions.py --samples 500` | Normal vs Skewed vs Heavy-tailed; why mean lies when tails are heavy |
| **Demo 1: Outlier Injection** | `python3 demos/demo1_distributions.py --outlier 500.0` | How a single 500° outlier doubles the mean while median stays unchanged |
| **Demo 2: Bayes Calculator** | `python3 demos/demo2_bayes_calculator.py --prevalence 0.01` | 10,000-person grid; base rate neglect; why a 90% accurate test yields only 9.17% posterior |
| **Demo 3: Sampling Bias** | `python3 demos/demo3_sampling_bias.py` | 20,000 voluntary survey respondents (biased) vs 500 random respondents |
| **Demo 3: Signal vs Noise** | `python3 demos/demo3_sampling_bias.py` | A/B testing: $n=2,000$ vs $n=20,000$ sample sizes and statistical significance |
| **Run All** | `bash demos/run_all.sh` | Executes all 3 morning demos in sequence |

---

## 6. Emergency Recovery

| Problem | Instant Fix |
|---|---|
| Reset all teaching progress | `bash scripts/reset.sh` |
| Candidates can't install libraries | Demos run with pure Python + standard NumPy with zero external C-dependencies |
| Candidate confused by Bayes formula | Point to Demo 2's 10,000-person natural frequency table |
