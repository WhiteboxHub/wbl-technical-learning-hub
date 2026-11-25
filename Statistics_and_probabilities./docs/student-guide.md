# Student Study Guide: Week 2 Day 1 AM
# Statistics & Probability for ML

Welcome to **Week 2 Day 1 Morning (AM)** of the Whitebox Learning Agentic AI Engineering curriculum.

---

## 1. Quick Start
```bash
# 1. Run automated setup
bash scripts/setup.sh

# 2. Run all morning demos
bash demos/run_all.sh

# 3. Practice with your AI coach
# Open your agent and type: "quiz me on stats"
```

---

## 2. Core Concepts Cheat Sheet

### Distributions & Skewness
- **Normal:** Symmetric bell curve ($\text{Mean} \approx \text{Median} \approx \text{Mode}$).
- **Right-Skewed:** Long tail extending to high values ($\text{Mean} > \text{Median}$). Examples: Household income, daily rainfall, cloud server costs.
- **Heavy-Tailed:** Tails decay slower than exponential; extreme values are regular occurrences. Examples: Web latency spikes (p99/p99.9), financial market shocks.

### Spread & Outliers
- **Mean:** Center of gravity $\bar{x} = \frac{1}{n} \sum x_i$. Sensitive to outliers.
- **Median:** 50th percentile. Robust against outliers.
- **Variance ($\sigma^2$):** Average squared deviation from the mean.
- **Standard Deviation ($\sigma$):** Square root of variance; in same units as data.
- **Interquartile Range (IQR):** $Q_3 - Q_1$ (middle 50% of data). Robust measure of spread.

### Conditional Probability & Bayes' Theorem
$$\mathbb{P}(A \mid B) = \frac{\mathbb{P}(B \mid A) \cdot \mathbb{P}(A)}{\mathbb{P}(B)}$$

#### The 10,000-Person Intuition
- **Total:** 10,000 people
- **Base Rate (1% prevalence):** 100 sick, 9,900 healthy
- **Test (90% sensitivity, 9% false positive rate):**
  - Sick testing positive (True Positives): $100 \times 0.90 = 90$
  - Healthy testing positive (False Positives): $9,900 \times 0.09 = 891$
- **Posterior Probability:**
  $$\mathbb{P}(\text{Sick} \mid +) = \frac{90}{90 + 891} = \frac{90}{981} \approx 9.17\%$$

### Sampling Bias
- **Selection Bias:** Samples collected in a way that some members are less likely to be included.
- **Non-Response Bias:** People who choose to respond differ systematically from those who do not.
- **Golden Rule:** **Size does not cure bias.** 1,000,000 biased records will only produce high confidence in a wrong answer.

### Signal vs Noise
- In A/B testing, an observed conversion lift could be a true improvement (**signal**) or random chance (**noise**).
- Sample size determines statistical power: small samples have high noise variance; large samples allow detection of genuine small effects.

---

## 3. Hands-On Exercises

### Exercise 1: Bayes Base-Rate Sensitivity Drill
Run the Bayes calculator with different base rates:
```bash
python3 demos/demo2_bayes_calculator.py --prevalence 0.001
python3 demos/demo2_bayes_calculator.py --prevalence 0.01
python3 demos/demo2_bayes_calculator.py --prevalence 0.10
```
**Task:** Record the resulting posterior probability for each run and write a 2-sentence explanation of why the posterior probability rises dramatically as prevalence increases.

### Exercise 2: Outlier Impact on Mean vs Median
Run the distribution demo with an extreme outlier:
```bash
python3 demos/demo1_distributions.py --samples 500 --outlier 1000.0
```
**Task:** Observe the percentage change in the Mean versus the Median. Why does this matter when reporting API response times to clients?

---

## 4. Evening Self-Test (Done-Check)

Answer these 5 questions with your practice coach (type `"quiz me on stats"`):
1. What is the fundamental difference between a right-skewed and a heavy-tailed distribution?
2. If you are training a model to predict house prices, should you optimize for mean squared error or mean absolute error if the target has extreme luxury mansions?
3. Calculate the posterior probability for a 10,000-person population with 2% prevalence, 95% sensitivity, and 5% false positive rate.
4. Why is a random sample of 500 voters more reliable than 50,000 voluntary online poll responses?
5. What does a p-value of 0.03 mean in an A/B test?

Record your verified results in `candidate-state.md`.
