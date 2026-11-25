#!/usr/bin/env python3
"""
Week 2 AM - Demo 2: The 10,000-Person Bayes Calculator Built Live
Story Anchor: The weather forecaster who is never certain, only honest about the odds.

Demonstrates:
- P(Positive) is NOT P(Disease | Positive)!
- Base rate fallacy: On a 1% base rate, a 90% accurate test yields ~9% real chance of disease.
- Teaches Bayes via natural frequencies (counts) instead of opaque symbolic algebra.

Variation to try live:
python demo2_bayes_calculator.py --prevalence 0.10
(Shows that when disease prevalence rises to 10%, a positive test reaches ~53% posterior probability!)
"""

import sys
import argparse


def print_box(text):
    print("┌" + "─" * 70 + "┐")
    for line in text.strip().split("\n"):
        print(f"│ {line.ljust(68)} │")
    print("└" + "─" * 70 + "┘")


def calculate_bayes(population=10000, prevalence=0.01, sensitivity=0.90, fpr=0.09):
    # Total sick and healthy
    sick_total = round(population * prevalence)
    healthy_total = population - sick_total

    # True Positives & False Negatives (among the sick)
    tp = round(sick_total * sensitivity)
    fn = sick_total - tp

    # False Positives & True Negatives (among the healthy)
    fp = round(healthy_total * fpr)
    tn = healthy_total - fp

    # Total Positive Tests
    total_positives = tp + fp

    # Posterior Probability P(Disease | Positive)
    p_disease_given_positive = (tp / total_positives) if total_positives > 0 else 0.0

    return {
        "population": population,
        "prevalence": prevalence,
        "sensitivity": sensitivity,
        "fpr": fpr,
        "sick_total": sick_total,
        "healthy_total": healthy_total,
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "tn": tn,
        "total_positives": total_positives,
        "posterior": p_disease_given_positive,
    }


def display_results(res):
    print("\n" + "=" * 72)
    print(" WEEK 2 AM — DEMO 2: BAYES CALCULATOR (NATURAL COUNTS) ".center(72, "="))
    print("=" * 72)
    print(f" Total Population Considered : {res['population']:,} people")
    print(f" Prior Prevalence (Base Rate): {res['prevalence']*100:.1f}%")
    print(f" Test Sensitivity (True Pos) : {res['sensitivity']*100:.1f}% of sick test positive")
    print(f" False Positive Rate (FPR)   : {res['fpr']*100:.1f}% of healthy mistakenly test positive")
    print("-" * 72)

    grid = f"""
                       TEST POSITIVE (+)    TEST NEGATIVE (-)     TOTAL
   SICK (Has Disease)        {res['tp']:>5} (TP)            {res['fn']:>5} (FN)        {res['sick_total']:>5}
   HEALTHY (No Disease)      {res['fp']:>5} (FP)            {res['tn']:>5} (TN)        {res['healthy_total']:>5}
   ---------------------------------------------------------------------
   TOTAL TESTS               {res['total_positives']:>5}                {res['fn']+res['tn']:>5}        {res['population']:>5}
    """
    print(grid)

    print("-" * 72)
    print(" STEP-BY-STEP INTUITION:")
    print(f"  1. Out of {res['population']:,} people, only {res['sick_total']:,} actually have the disease.")
    print(f"  2. Of those {res['sick_total']:,} sick people, {res['tp']} test POSITIVE.")
    print(f"  3. But among the {res['healthy_total']:,} healthy people, {res['fpr']*100:.1f}% also test POSITIVE = {res['fp']} false alarms!")
    print(f"  4. Total people testing positive = {res['tp']} (true) + {res['fp']} (false) = {res['total_positives']}.")
    print(f"  5. Probability you are actually sick given a positive test:")
    print(f"       P(Sick | Positive) = {res['tp']} / {res['total_positives']} = {res['posterior']*100:.2f}%\n")

    summary = f"""
    THE VERDICT:
    If a patient gets a POSITIVE result from this 90% accurate test,
    their chance of actually having the disease is ONLY {res['posterior']*100:.2f}%!
    Most people guess 90%, completely ignoring the 1% base rate.
    """
    print_box(summary)


def main():
    parser = argparse.ArgumentParser(description="Demo 2: 10,000-Person Bayes Calculator")
    parser.add_argument("--population", type=int, default=10000, help="Total population size (default: 10000)")
    parser.add_argument("--prevalence", type=float, default=0.01, help="Base rate prevalence (default: 0.01 = 1%%)")
    parser.add_argument("--sensitivity", type=float, default=0.90, help="Test sensitivity (default: 0.90 = 90%%)")
    parser.add_argument("--fpr", "--fp-rate", type=float, default=0.09, dest="fpr", help="False positive rate (default: 0.09 = 9%%)")
    args = parser.parse_args()

    results = calculate_bayes(
        population=args.population,
        prevalence=args.prevalence,
        sensitivity=args.sensitivity,
        fpr=args.fpr
    )
    display_results(results)


if __name__ == "__main__":
    main()

