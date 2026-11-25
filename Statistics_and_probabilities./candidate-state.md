# CANDIDATE STATE - [Candidate Name]
Program: Whitebox Learning - Agentic AI Engineering
Track: Week 2 Day 1 AM (Statistics & Probability for ML)
Platform I mainly use: Claude / Antigravity / Cursor / Codex / Grok
Level band: Ready

## Progress
- Current Session: Week 2 Day 1 Morning (AM)
- Topic: Statistics & Probability for ML
- Story Anchor: *The weather forecaster who is never certain, only honest about the odds*
- Concepts covered:
  - [ ] Distributions: Normal, Right-Skewed, Heavy-Tailed shapes
  - [ ] Spread: Mean, Variance, Std Dev, Median, IQR (why mean alone misleads)
  - [ ] Probability: $P(A)$, Joint $P(A \cap B)$, Conditional $P(A \mid B)$
  - [ ] Bayes' Theorem: Updating prior beliefs with natural frequency counts (10,000 people)
  - [ ] Sampling Bias: Selection, non-response, survivorship; why sample size cannot cure bias
  - [ ] Hypothesis Thinking: Signal vs noise in A/B testing ($n=2,000$ vs $n=20,000$)
- Topics I can explain without notes: [Update after practice session]

## Work & Verification Evidence
- Assignments completed:
  - [ ] Demo 1: Run `python3 demos/demo1_distributions.py` and inspect outlier shift
  - [ ] Demo 2: Run `python3 demos/demo2_bayes_calculator.py` with custom `--prevalence`
  - [ ] Demo 3: Run `python3 demos/demo3_sampling_bias.py` and compare $n=20,000$ biased vs $n=500$ random
  - [ ] Automated Smoke Test: `bash scripts/smoke.sh` passing
- Code written / repo folder:
  - `demos/demo1_distributions.py`
  - `demos/demo2_bayes_calculator.py`
  - `demos/demo3_sampling_bias.py`
  - `data/medical_screening_sample.csv`
  - `data/weather_forecaster_survey.csv`

## Results & Self-Check (Done-Check)
- Quiz results: [e.g. 5/5 on morning stats check]
- Done-Check Evaluation:
  - [ ] Question 1: Explain normal vs skewed vs heavy-tailed distributions and name an ML domain for each
  - [ ] Question 2: Why does the mean alone mislead when reporting latencies or incomes?
  - [ ] Question 3: 10,000 people, 1% prevalence, 90% sensitivity, 9% false positive rate — calculate $P(\text{Sick} \mid +)$
  - [ ] Question 4: Why can 100,000 voluntary survey respondents be more wrong than 500 randomly sampled ones?
  - [ ] Question 5: What does "signal versus noise" mean for an A/B test?
- Weak areas identified: [List specific concepts needing review]
- Strong areas: [Concepts mastered]

## Open Questions & Instructor Bridge
- Open questions for instructor:
  1. [Candidate question]
- Things I am stuck on right now: None
- Next session: Monday PM (ML Lifecycle + MLflow Experiment Tracking)

Last updated: [Date], by [Agent / Candidate Name]
