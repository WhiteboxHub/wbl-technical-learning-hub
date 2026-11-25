#!/usr/bin/env python3
"""
Week 2 AM - Demo 3: Biased vs Random Sampling & Signal vs Noise
Story Anchor: The weather forecaster who is never certain, only honest about the odds.

Demonstrates:
Part 1 - Sampling Bias:
  Why a biased poll with 20,000 answers is WORSE than an unbiased random sample of 500.
  Size does not cure bias!

Part 2 - Signal vs Noise:
  Simulates an A/B test with a true 1% conversion lift (Control: 10.0%, Variant: 11.0%).
  - At n = 2,000 users per group: the 1% lift is drowned in noise (p-value > 0.05).
  - At n = 20,000 users per group: the same 1% lift becomes a clear, detectable signal (p-value < 0.001).

Run:
  python demo3_sampling_bias.py
"""

import sys
import argparse
import numpy as np

try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def print_banner(title):
    width = 75
    print("\n" + "=" * width)
    print(f" {title} ".center(width, "="))
    print("=" * width)


def demo_sampling_bias():
    print_banner("PART 1: SAMPLING BIAS (SIZE DOES NOT FIX BIAS)")
    np.random.seed(42)

    # True population: 1,000,000 customers
    # True metric: 30% satisfaction across the whole country
    N = 1_000_000
    true_rate = 0.30
    population = np.random.binomial(n=1, p=true_rate, size=N)

    # Suppose satisfied customers are 3x more likely to respond to an online voluntary survey (selection bias)
    response_prob = np.where(population == 1, 0.60, 0.20)
    biased_respondents = population[np.random.random(N) < response_prob]

    # Sample A: Big biased voluntary sample of 20,000
    sample_biased_20k = np.random.choice(biased_respondents, size=20_000, replace=False)

    # Sample B: Small, properly randomized scientific sample of 500
    sample_random_500 = np.random.choice(population, size=500, replace=False)

    print(f" True Population Mean Satisfaction : {np.mean(population)*100:.2f}%\n")
    print(f" [A] Voluntary Survey (n = 20,000)  : {np.mean(sample_biased_20k)*100:.2f}% (ERROR: +{abs(np.mean(sample_biased_20k)-true_rate)*100:.2f}%)")
    print(f" [B] Simple Random Sample (n = 500) : {np.mean(sample_random_500)*100:.2f}% (ERROR: {abs(np.mean(sample_random_500)-true_rate)*100:.2f}%)")

    print("\nTAKEAWAY FOR ML ENGINEERS:")
    print("  Adding 10x more data to a biased dataset only gives you high confidence")
    print("  in the wrong answer! Always check selection and non-response bias first.")


def demo_signal_vs_noise():
    print_banner("PART 2: SIGNAL VERSUS NOISE IN A/B TESTING")
    np.random.seed(101)

    # Control has 10.0% conversion; Treatment has 11.0% conversion (True lift = 1.0%)
    p_control = 0.10
    p_variant = 0.11
    true_lift = (p_variant - p_control) * 100

    print(f" True Ground Truth: Control = {p_control*100:.1f}%, Variant = {p_variant*100:.1f}% (True Lift = +{true_lift:.1f}%)\n")

    for n in [2000, 20000]:
        ctrl = np.random.binomial(n=1, p=p_control, size=n)
        var = np.random.binomial(n=1, p=p_variant, size=n)

        c_rate = np.mean(ctrl) * 100
        v_rate = np.mean(var) * 100
        observed_lift = v_rate - c_rate

        # Standard error of difference in proportions
        se = np.sqrt((c_rate * (100 - c_rate) / n) + (v_rate * (100 - v_rate) / n))
        z_score = observed_lift / se if se > 0 else 0

        # Normal approx two-tailed p-value
        if HAS_SCIPY:
            p_val = 2 * (1 - stats.norm.cdf(abs(z_score)))
        else:
            # Simple approximation
            p_val = np.exp(-0.717 * z_score - 0.416 * (z_score**2)) if z_score > 0 else 1.0

        decision = "STATISTICALLY SIGNIFICANT (Signal)" if p_val < 0.05 else "INCONCLUSIVE / NOISE (Chance cannot be ruled out)"

        print(f"--- Experiment Sample Size n = {n:,} per branch ---")
        print(f"  Observed Control Conversion : {c_rate:5.2f}%")
        print(f"  Observed Variant Conversion : {v_rate:5.2f}%")
        print(f"  Observed Absolute Lift      : {observed_lift:+5.2f}%")
        print(f"  Z-score: {z_score:5.2f} | Approx p-value: {p_val:.4f}")
        print(f"  Conclusion                  : {decision}\n")

    print("-" * 75)
    print("EXIT CHECK QUESTION:")
    print("  'What does signal versus noise mean for an A/B result?'")
    print("  Answer: Whether the observed difference is larger than chance variation alone")
    print("          would produce given the sample size.")
    print("-" * 75)


def main():
    demo_sampling_bias()
    demo_signal_vs_noise()


if __name__ == "__main__":
    main()

