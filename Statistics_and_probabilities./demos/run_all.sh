#!/usr/bin/env bash
# Run all Statistics & Probability demos for Week 2 Day 1 AM
set -euo pipefail
cd "$(dirname "$0")/.."

say()  { printf '%s\n' "$*"; }
step() { printf '\n======================================================\n%s\n======================================================\n' "$*"; }

step "Demo 1: Distributions, Skewness, Outliers & Spread"
python3 demos/demo1_distributions.py --samples 500

step "Demo 2: Conditional Probability & Bayes' Theorem Calculator"
python3 demos/demo2_bayes_calculator.py --prevalence 0.01 --sensitivity 0.95 --fp-rate 0.05

step "Demo 3: Sampling Bias & Signal vs Noise (A/B Test)"
python3 demos/demo3_sampling_bias.py

step "ALL DEMOS EXECUTED SUCCESSFULLY"
say "All 3 Monday AM Statistics & Probability demos completed without error."

