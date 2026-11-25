# Module 1 — Statistics & Probability for ML (Week 2 AM Day 1)

Teach-skill content file. Format is described in `skills/stats-skill/SKILL.md`.  
Deck: `ML Fundamentals` (Probability: slides 9–38, Statistics: slides 39–68) & `Essential Math for ML`.  
Story Anchor: **The weather forecaster who is never certain, only honest about the odds.**  
Environment: Python 3.10+ with `numpy`, `scipy`, `matplotlib` (`scripts/setup.sh` must be READY).  
Time: ~180 minutes (Intro: 15m, Topics: 150m, Conclusion: 15m).

## Objectives
By the end of this session, candidates can:
1. Read a distribution plot and state what its shape implies for model training and loss functions.
2. Explain Bayes' Theorem with a concrete worked example (counts, no formula-reciting).
3. Name three ways a sample can lie (selection, non-response, survivorship) and how each is detected.
4. Distinguish signal from noise in experiment and A/B test results.

---

### Beat 1.1 — The Weather Forecaster: Calibration vs Certainty
- **Slides:** 6–7 (Common questions about math; Contents in Math for ML)
- **Say:**
  - A forecast is an honest statement about uncertainty, not a promise.
  - When a forecaster says "70% chance of rain", if it does not rain, they weren't necessarily wrong. If it rains 7 out of 10 times they say 70%, their model is well-calibrated.
  - Every machine learning model you train later is a betting engine. Today is where you learn how to price a bet without lying to yourself.
- **Ask:**
  - Q: If it rains on a day with a 30% rain forecast, was the forecaster wrong? — A: No; 30% means it will rain 3 out of 10 such days. A single outcome cannot invalidate a probability.
- **Done when:** Candidates articulate that probabilities reflect calibrated uncertainty rather than guarantees.

### Beat 1.2 — Reading Distribution Shapes: Normal, Skewed, Heavy-Tailed
- **Slides:** 27 (Random Variables), 34–37 (Binomial), 184–186 (Distributions, Outliers, Box Plot)
- **Say:**
  - Three shapes dominate real data: Normal (symmetric), Right-Skewed (income, rainfall), and Heavy-Tailed (latencies, losses, rare catastrophes).
  - In a Normal distribution, Mean ≈ Median ≈ Mode.
  - In a Right-Skewed distribution, extreme high values pull the Mean above the Median.
  - In Heavy-Tailed distributions (Pareto), rare extreme events dominate the variance and can destroy model loss functions like MSE.
- **Demo (run: agent):**
  ```bash
  python3 demos/am/demo1_distributions.py --samples 10000
  ```
  **Point out:** Compare the mean vs median in normal vs skewed vs pareto. Notice how skewed mean is noticeably larger than median.
- **Ask:**
  - Q: If the mean salary in a company is $120k but the median is $65k, what is the shape of the salary distribution? — A: Right-skewed; a few very high earners pull the mean up.
  - Q: Why is Mean Squared Error (MSE) risky on heavy-tailed data? — A: Squaring huge tail values makes a few extreme outliers dominate all gradient updates.
- **Done when:** Candidates can look at a summary or histogram and explain the difference between mean and median.

### Beat 1.3 — Mean, Variance and Spread: Why the Mean Alone Misleads
- **Slides:** 57–66 (Mean, Median, Mode, Variance, Standard Deviation)
- **Say:**
  - Mean tells you where the center of mass is; variance and standard deviation tell you how much to trust that center.
  - Two delivery routes can both average 30 minutes: Route A varies ±2 minutes (28–32m); Route B varies ±25 minutes (5–55m). Same mean, totally different business promise!
  - Outliers: Never delete an outlier on sight! An outlier can be a data entry error, a sensor fault, or the exact fraud you were hired to detect.
- **Demo (run: agent):**
  ```bash
  python3 demos/am/demo1_distributions.py --outlier 500.0
  ```
  **Point out:** Look at how a single extreme outlier shifts the mean while leaving the median unchanged.
- **Ask:**
  - Q: Two models both have an average error of 5. Model 1 std dev is 1; Model 2 std dev is 15. Which is safer for production? — A: Model 1; it is consistent and predictable.
- **Done when:** Candidates explain that spread determines reliability.

### Beat 1.4 — Probability & Conditional Probability: P(A) is not P(A | B)
- **Slides:** 17 (Dependent Events), 22–26 (Conditional and Joint Probability)
- **Say:**
  - P(A) is the unconditional probability in the whole world.
  - P(A | B) shrinks the universe strictly to the cases where B actually occurred.
  - The probability tree makes the denominator visible. Never confuse P(Spam | contains "Free") with P(contains "Free" | Spam).
- **Ask:**
  - Q: What does conditioning on B do to your denominator? — A: It shrinks the denominator from the entire population to only the subset where event B happened.
- **Done when:** Candidates explain the difference between joint and conditional probabilities.

### Beat 1.5 — Bayes and Base Rates: The 10,000-Person Medical Screening
- **Slides:** 28–33 (Bayes' Theorem derivation & worked example), 295–296 (Bayes and Imbalanced Datasets)
- **Say:**
  - Bayes in plain counts, never abstract Greek letters first:
    - 10,000 people total.
    - Prevalence is 1% → 100 are sick, 9,900 are healthy.
    - Test has 90% sensitivity → 90 of the 100 sick test positive (10 missed).
    - Test has 9% false positive rate → 9% of 9,900 healthy test positive = 891 false alarms!
    - Total positive tests = 90 + 891 = 981.
    - Chance you are sick given a positive test = 90 / 981 ≈ 9.18%!
  - Almost every engineer guesses 90% because they forget the massive healthy base rate.
- **Demo (run: agent):**
  ```bash
  python3 demos/am/demo2_bayes_calculator.py --prevalence 0.01
  python3 demos/am/demo2_bayes_calculator.py --prevalence 0.10
  ```
  **Point out:** When prevalence is 1%, P(Sick|Positive) is ~9%. When prevalence rises to 10%, P(Sick|Positive) jumps to ~53%!
- **Ask:**
  - Q: Why can a 99% accurate test produce mostly false alarms on a rare fraud transaction? — A: Base rate: Because 99.9% of transactions are legitimate, 1% of the legitimate majority easily outnumbers the real fraud.
- **Done when:** Candidates can explain the 10,000-person calculation without reciting formulas.

### Beat 1.6 — Sampling & Bias: How a Large Sample Still Lies
- **Slides:** 47–53 (Sampling Techniques, Stratified, Non-Probability Sampling)
- **Say:**
  - Three deadly biases:
    1. **Selection Bias**: Who has the chance to be in the sample.
    2. **Non-Response Bias**: Who chooses to answer (usually angry or delighted users).
    3. **Survivorship Bias**: Looking only at what survived the process (e.g. reviewing only successful loan applicants).
  - Size does NOT fix bias. A biased poll of 20,000 people gives high confidence in a completely wrong answer!
- **Demo (run: agent):**
  ```bash
  python3 demos/am/demo3_sampling_bias.py
  ```
  **Point out:** See Part 1 output: The voluntary survey of 20,000 people is off by over 15%, while a tiny random sample of 500 is within 2%.
- **Ask:**
  - Q: A food delivery app sends an email survey. 50,000 people reply with an average score of 2/5. Is that the customer satisfaction? — A: No; non-response bias. Only people with bad orders took the time to complain.
- **Done when:** Candidates can name the three biases and explain why sample size does not cure them.

### Beat 1.7 — Hypothesis Thinking: Signal vs Noise
- **Slides:** 54–56 (Types of Statistics; Signal vs Noise)
- **Say:**
  - In A/B testing or ML evaluations, every observed difference is either real (signal) or chance variation (noise).
  - More data shrinks noise (standard error drops as 1 / sqrt(n)), but does NOT shrink bias.
  - A 1% lift at n=2,000 is noise. The exact same 1% lift at n=20,000 is undeniable signal.
- **Demo (run: agent):**
  ```bash
  python3 demos/am/demo3_sampling_bias.py
  ```
  **Point out:** See Part 2 output: At n=2,000, p-value is > 0.10 (noise). At n=20,000, p-value is < 0.001 (signal).
- **Ask:**
  - Q: What does "signal versus noise" mean for an A/B test? — A: Whether the observed difference is larger than chance variation alone would produce given the sample size.
- **Done when:** Candidates explain how sample size impacts confidence in an observed effect.

---

## Exercise (Candidate Afternoon / Evening Task)
1. Run `python3 demos/am/demo2_bayes_calculator.py` with your own altered prevalence (e.g. `--prevalence 0.05`). Record the table and write a 2-sentence explanation of why the posterior probability changed.
2. Write a one-paragraph reflection naming a real-world example of sampling bias (selection, non-response, or survivorship) that you have observed in an app or job.

## Done-Check
1. Why can a 95%-accurate test still be wrong most of the time when it says positive?
   - *Pass criteria:* Explains base rate: false positives from the large healthy population outnumber true positives from the rare sick population.
2. Name three ways a sample can lie and how each is caught.
   - *Pass criteria:* Names selection, non-response, and survivorship bias with a detection strategy.
3. Two datasets have the same mean. What else do you need before deciding they are alike?
   - *Pass criteria:* Spread (variance / standard deviation / IQR) and shape (distribution plot).
4. What does "signal versus noise" mean for an A/B result?
   - *Pass criteria:* Distinguishing real underlying differences from random sampling variation.

## Clean-Up
`scripts/reset.sh`

