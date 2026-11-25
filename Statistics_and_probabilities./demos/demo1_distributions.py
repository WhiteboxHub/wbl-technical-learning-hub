#!/usr/bin/env python3
"""
Week 2 AM - Demo 1: Three Distributions (Normal, Right-Skewed, Heavy-Tailed)
Story Anchor: The weather forecaster who is never certain, only honest about the odds.

This demo generates three realistic datasets:
1. Daily Temperature (Normal / Gaussian)
2. Household Income / Rainfall Volume (Right-Skewed / Log-Normal)
3. Website Latency / Severity of Insurance Claims (Heavy-Tailed / Pareto)

Shows:
- Why mean alone misleads: In skewed/heavy-tailed shapes, mean is pulled far from median.
- Prints large readable output suitable for in-class demonstration.
- Saves comparison plot to 'distributions_comparison.png'.

Variation to try live:
python demo1_distributions.py --outlier 500.0
"""

import sys
import argparse
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def print_banner(title):
    width = 75
    print("\n" + "=" * width)
    print(f" {title.upper()} ".center(width, "="))
    print("=" * width)


def describe_data(name, data):
    mean_val = float(np.mean(data))
    median_val = float(np.median(data))
    std_val = float(np.std(data))
    q25, q75 = float(np.percentile(data, 25)), float(np.percentile(data, 75))
    iqr_val = q75 - q25
    skew_direction = "SYMMETRIC (Mean ≈ Median)" if abs(mean_val - median_val) < 0.25 * std_val else (
        "RIGHT-SKEWED (Mean > Median)" if mean_val > median_val else "LEFT-SKEWED (Mean < Median)"
    )

    print(f"\n--- {name} ---")
    print(f"  Sample Size (n)   : {len(data):,}")
    print(f"  Mean (Average)    : {mean_val:10.2f}   <-- Pulled by tails/extremes")
    print(f"  Median (50th %ile): {median_val:10.2f}   <-- Robust typical value")
    print(f"  Spread: Std Dev   : {std_val:10.2f} | IQR: {iqr_val:10.2f}")
    print(f"  Shape Diagnosis   : {skew_direction}")
    return mean_val, median_val, std_val


def main():
    parser = argparse.ArgumentParser(description="Demo 1: Reading Distribution Shapes")
    parser.add_argument("--samples", type=int, default=10000, help="Number of samples (default: 10000)")
    parser.add_argument("--outlier", type=float, default=None, help="Inject an extreme outlier to show mean distortion")
    args = parser.parse_args()

    np.random.seed(42)
    n = args.samples

    print_banner("Week 2 AM — Demo 1: Reading Distribution Shapes")
    print("Teaching Point: The mean says where the balance point is, but the median says")
    print("where the typical person or day lives. In skewed distributions, the mean lies!\n")

    # 1. Normal Distribution (Daily Temperatures in Celsius, mean=22, std=4)
    normal_data = np.random.normal(loc=22.0, scale=4.0, size=n)

    # 2. Right-Skewed Distribution (Log-normal: Daily Rainfall or Income in $k)
    # meanlog=3.0, sdlog=0.7 -> mean around 25, long right tail
    skewed_data = np.random.lognormal(mean=3.0, sigma=0.75, size=n)

    # 3. Heavy-Tailed Distribution (Pareto: Server Latency ms or Claim Size)
    # alpha=2.2 (mild heavy tail, extreme values occur regularly)
    pareto_data = (np.random.pareto(a=2.2, size=n) + 1.0) * 15.0

    if args.outlier is not None:
        print(f"[!] INJECTING DELIBERATE EXTREME VALUE: {args.outlier} into normal dataset!")
        normal_data[-1] = args.outlier

    # Output stats
    describe_data("1. NORMAL (Daily Temperature °C)", normal_data)
    describe_data("2. RIGHT-SKEWED (Income / Rainfall)", skewed_data)
    describe_data("3. HEAVY-TAILED (Latency ms / Claims)", pareto_data)

    print("\n" + "-" * 75)
    print("CLASS CHECK QUESTION:")
    print("  'If an insurer prices insurance based purely on the mean claim size,")
    print("   what happens when a single heavy-tailed 1-in-1,000 claim hits?'")
    print("Expected: The single extreme claim blows up the average and ruins the forecast.")
    print("-" * 75)

    if HAS_MATPLOTLIB:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Plot 1: Normal
        axes[0].hist(normal_data, bins=40, color="#2b5c8f", edgecolor="white", alpha=0.8)
        axes[0].axvline(np.mean(normal_data), color="red", linestyle="--", linewidth=2, label=f"Mean: {np.mean(normal_data):.1f}")
        axes[0].axvline(np.median(normal_data), color="green", linestyle="-", linewidth=2, label=f"Median: {np.median(normal_data):.1f}")
        axes[0].set_title("Normal Distribution (Symmetric)")
        axes[0].legend()

        # Plot 2: Right-Skewed
        axes[1].hist(skewed_data[skewed_data < np.percentile(skewed_data, 99)], bins=40, color="#d95f02", edgecolor="white", alpha=0.8)
        axes[1].axvline(np.mean(skewed_data), color="red", linestyle="--", linewidth=2, label=f"Mean: {np.mean(skewed_data):.1f}")
        axes[1].axvline(np.median(skewed_data), color="green", linestyle="-", linewidth=2, label=f"Median: {np.median(skewed_data):.1f}")
        axes[1].set_title("Right-Skewed Distribution")
        axes[1].legend()

        # Plot 3: Heavy-Tailed
        axes[2].hist(pareto_data[pareto_data < np.percentile(pareto_data, 98)], bins=40, color="#7570b3", edgecolor="white", alpha=0.8)
        axes[2].axvline(np.mean(pareto_data), color="red", linestyle="--", linewidth=2, label=f"Mean: {np.mean(pareto_data):.1f}")
        axes[2].axvline(np.median(pareto_data), color="green", linestyle="-", linewidth=2, label=f"Median: {np.median(pareto_data):.1f}")
        axes[2].set_title("Heavy-Tailed (Pareto) Distribution")
        axes[2].legend()

        output_plot = "distributions_comparison.png"
        plt.tight_layout()
        plt.savefig(output_plot, dpi=120)
        print(f"\n[✓] Saved distribution comparison visual plot to '{output_plot}'")
    else:
        print("\n[NOTE] Matplotlib not installed; printed numerical diagnostics only.")


if __name__ == "__main__":
    main()

