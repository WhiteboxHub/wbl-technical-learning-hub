# Instructor Guide: Week 2 Day 1 AM
# Statistics & Probability for ML

Complete instructor reference manual for teaching **Week 2 Day 1 Morning (AM)** of the Whitebox Learning Agentic AI Engineering curriculum.

---

## 1. Session Architecture & Narrative

- **Topic:** Statistics & Probability for ML
- **Story Anchor:** *The weather forecaster who is never certain, only honest about the odds.*
  A forecast of "70% chance of rain" is an honest statement about uncertainty, not a broken promise when it stays sunny 3 out of 10 times. In ML engineering, models produce probabilities, not certainties. If you do not understand distributions, base rates, and sampling bias, your models will confidently fail in production.
- **Duration:** 3 hours (180 minutes)

### Time Allocation Breakdown
| Act | Duration | Focus |
|---|---|---|
| **Act 1: The Shape of Data** | 50 mins | Story anchor, Normal vs Skewed vs Heavy-Tailed distributions, Spread, Mean vs Median, Outlier injection. Demo 1. |
| **Act 2: Uncertainty & Bayes** | 50 mins | Joint vs conditional probability, Bayes' Theorem, base rate fallacy, 10,000-person medical screening grid. Demo 2. |
| **Break** | 10 mins | Coffee & informal discussion. |
| **Act 3: Sampling & Decisions** | 50 mins | Sampling bias (selection, non-response, survivorship), why size cannot cure bias, signal vs noise in A/B testing. Demo 3. |
| **Conclusion & Handover** | 20 mins | Exercise handover, Done-check questions, updating `candidate-state.md`. |

---

## 2. Beat-by-Beat Instructor Script

### Beat 1.1 — The Weather Forecaster & Uncertainty
- **Core Concept:** Probability as degree of belief and frequency of occurrence under uncertainty.
- **Talking Points:**
  - Machine learning models do not output facts; they output scores or probability distributions.
  - A classifier outputting `0.92` probability of fraud is not 100% sure; it asserts that in 92 out of 100 similar cases, fraud occurs.
  - An engineer who treats model scores as binary booleans causes catastrophic threshold failures.
- **Check Question:** "If an ML model predicts 80% probability of rain and it doesn't rain, was the model wrong?"
- **Answer:** No. 80% means rain happens 8 out of 10 times; dry days happen 2 out of 10 times. A single outcome never proves or disproves a probabilistic prediction.

### Beat 1.2 — Reading the Shape of Data
- **Core Concept:** Normal, skewed, and heavy-tailed distributions.
- **Demo:** `python3 demos/demo1_distributions.py --samples 500`
- **Key Takeaways:**
  - **Normal (Gaussian):** Bell curve, symmetric, mean $\approx$ median. Typical of physical measurements (temperature, height).
  - **Right-Skewed:** Long tail to the right, mean $>$ median. Typical of financial transactions, customer lifetime value, rainfall.
  - **Heavy-Tailed (Power Law / Pareto):** Extreme events occur far more often than Gaussian models assume. Typical of network latencies, API request spikes, insurance claims.
- **Check Question:** "Why do web servers experience 99th-percentile latency spikes that Gaussian assumptions fail to predict?"
- **Answer:** Server requests follow heavy-tailed distributions; rare cascade timeouts produce extreme outliers that a bell curve predicts would happen once in a billion years.

### Beat 1.3 — Spread: Why the Mean Lies
- **Core Concept:** Mean vs median, standard deviation, interquartile range (IQR), and outlier sensitivity.
- **Demo:** `python3 demos/demo1_distributions.py --outlier 500.0`
- **Key Takeaways:**
  - The mean is the center of gravity (balance point); a single extreme value pulls it violently.
  - The median is the 50th percentile; it is robust against outliers.
  - When data is skewed or heavy-tailed, reporting only the mean is professional negligence.
- **Check Question:** "If an insurer prices policies based on the mean claim size of \$5,000, what happens when a single \$1,000,000 claim hits?"
- **Answer:** The insurer becomes insolvent. The mean was driven by normal days and completely missed the heavy tail.

### Beat 1.4 — Conditional Probability & Bayes' Theorem
- **Core Concept:** Prior probability, likelihood, evidence, and posterior probability.
- **Demo:** `python3 demos/demo2_bayes_calculator.py --prevalence 0.01 --sensitivity 0.90 --fpr 0.09`
- **Natural Frequency Table (10,000 people):**
  - Disease Prevalence: 1% $\rightarrow$ 100 sick, 9,900 healthy.
  - Test Sensitivity: 90% $\rightarrow$ 90 sick test positive, 10 false negatives.
  - False Positive Rate: 9% $\rightarrow$ $9,900 \times 0.09 = 891$ healthy test positive (false alarms).
  - Total positive tests: $90 + 891 = 981$.
  - True probability of sickness given positive test: $90 / 981 = 9.17\%$.
- **Check Question:** "Why does a 90% accurate test leave a patient with only a 9.17% chance of being sick?"
- **Answer:** Because the disease is rare (1% base rate). The massive pool of healthy people generates far more false alarms (891) than the small pool of sick people generates true positives (90).

### Beat 1.5 — Sampling Bias: Size Does Not Fix Bias
- **Core Concept:** Selection bias, non-response bias, survivorship bias.
- **Demo:** `python3 demos/demo3_sampling_bias.py` (Part 1)
- **Key Takeaways:**
  - A voluntary customer satisfaction survey of 20,000 respondents reported 56% satisfaction.
  - A rigorous random sample of only 500 customers reported 28% satisfaction.
  - True population ground truth: 30%.
  - Adding 10x more data to a biased collection mechanism only gives high statistical confidence in an erroneous number.
- **Check Question:** "If your training dataset has 1,000,000 phone survey responses, why might an unweighted model fail on election day?"
- **Answer:** Non-response and selection bias: people who answer unknown phone calls do not represent the general voting population.

### Beat 1.6 — Hypothesis Thinking: Signal vs Noise
- **Core Concept:** Sampling variability, standard error, z-scores, p-values in A/B testing.
- **Demo:** `python3 demos/demo3_sampling_bias.py` (Part 2)
- **Key Takeaways:**
  - With $n=2,000$, a +1.0% observed conversion difference might have high p-value (chance variation).
  - With $n=20,000$, the same true effect produces a low p-value (statistically distinguishable from noise).
- **Check Question:** "What does 'signal versus noise' mean for an A/B test result?"
- **Answer:** Whether the observed difference between variant and control is larger than chance random variation would produce given the sample size.

### Beat 1.7 — Hands-On Exercise & Exit Check
- Hand over exercise prompts and walk through Done-check criteria.

---

## 3. Exit Done-Check Rubric

| Question | Passing Criterion | Failure Criterion |
|---|---|---|
| **1. Distribution Shapes** | Distinguishes normal (symmetric), skewed (asymmetric tail), heavy-tailed (extreme outliers) with valid ML examples. | Confuses skewed with bimodal; claims all real data is normal. |
| **2. Mean vs Median** | Explains that mean is pulled by extreme values; median represents typical value in skewed data. | Claims mean is always superior or cannot explain outlier impact. |
| **3. Bayes Calculation** | Correctly computes $\approx 9.17\%$ using natural counts out of 10,000. | Guesses 90% or ignores base rate. |
| **4. Sampling Bias** | Explains that sample size increases precision but does not eliminate systematic collection bias. | Claims large sample size overcomes selection bias. |
| **5. Signal vs Noise** | Explains difference between real causal effect and random sampling fluctuation based on sample size. | Believes any positive lift proves the variant is better. |
