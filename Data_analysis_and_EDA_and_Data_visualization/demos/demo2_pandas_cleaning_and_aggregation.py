#!/usr/bin/env python3
"""
Demo 2: Pandas Data Ingestion, Cleaning, Filtering, and Aggregation
===================================================================
Story Anchor: 'Pandas is the workbench with labelled drawers.'
Topics Covered:
  - Reading CSV, handling missing values, dtype conversions
  - loc vs iloc indexing
  - Boolean multi-condition filtering (&, |, ~, str.contains)
  - Missing value diagnosis & imputations (isna, fillna, dropna)
  - GroupBy multi-aggregations and summary statistics
"""

import os
import csv
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
EMP_CSV = os.path.join(DATA_DIR, "employee_data.csv")

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def header(title: str):
    print(f"\n{'='*70}\n[PANDAS DEMO] {title}\n{'='*70}")

def run_pandas_mode():
    header("1. Loading Dirty Data & Diagnosing Nulls (Pandas Engine)")
    df = pd.read_csv(EMP_CSV)
    print("Initial Shape:", df.shape)
    print("\nMissing values per column:")
    print(df.isna().sum())
    
    header("2. Dtype Conversions & Cleaning")
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["Senior Management"] = df["Senior Management"].astype("boolean")
    df["First Name"] = df["First Name"].fillna("Unknown")
    df["Gender"] = df["Gender"].fillna("Not Specified")
    df["Team"] = df["Team"].fillna("Unassigned")
    print("After cleaning & imputation, missing count:", df.isna().sum().to_dict())
    
    header("3. Indexing: loc vs iloc")
    print("iloc[0:3, 0:4] (Pure integer position-based):")
    print(df.iloc[0:3, 0:4])
    print("\nloc[0:2, ['First Name', 'Salary', 'Team']] (Label/Condition-based):")
    print(df.loc[0:2, ['First Name', 'Salary', 'Team']])
    
    header("4. Complex Boolean Filtering")
    cond1 = (df["Gender"] == "Female") & (df["Team"] == "Engineering")
    cond2 = (df["Salary"] > 100000) & (df["Bonus %"] > 10.0)
    filtered = df[cond1 | cond2]
    print(f"Found {len(filtered)} matching candidates:")
    print(filtered[["First Name", "Gender", "Team", "Salary", "Bonus %"]])
    
    header("5. GroupBy & Multi-Metric Aggregations")
    team_summary = df.groupby("Team").agg(
        headcount=("Salary", "count"),
        avg_salary=("Salary", "mean"),
        max_salary=("Salary", "max")
    ).reset_index()
    team_summary["avg_salary"] = team_summary["avg_salary"].round(2)
    print(team_summary.to_string(index=False))

def run_fallback_mode():
    header("1. Loading Dirty Data & Diagnosing Nulls (Built-in Tabular Engine)")
    rows = []
    with open(EMP_CSV, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    
    print(f"Loaded {len(rows)} rows from {EMP_CSV}")
    
    # Null diagnosis
    headers = list(rows[0].keys())
    null_counts = {h: sum(1 for r in rows if not r[h].strip()) for h in headers}
    print("Missing values per column:")
    for h, cnt in null_counts.items():
        print(f"  {h:20s}: {cnt}")
        
    header("2. Data Cleaning & Imputation")
    for r in rows:
        if not r["First Name"].strip():
            r["First Name"] = "Unknown"
        if not r["Gender"].strip():
            r["Gender"] = "Not Specified"
        if not r["Team"].strip():
            r["Team"] = "Unassigned"
        r["Salary"] = float(r["Salary"]) if r["Salary"] else 0.0
        r["Bonus %"] = float(r["Bonus %"]) if r["Bonus %"] else 0.0
    print("Cleaned and imputed missing fields successfully.")
    
    header("3. Indexing & Multi-Condition Filtering")
    # Female Engineering OR Salary > 100k with Bonus > 10%
    matches = [
        r for r in rows
        if (r["Gender"] == "Female" and r["Team"] == "Engineering") or
           (r["Salary"] > 100000 and r["Bonus %"] > 10.0)
    ]
    print(f"Found {len(matches)} matching candidates:")
    for m in matches:
        print(f"  {m['First Name']:10s} | {m['Gender']:13s} | {m['Team']:15s} | ${m['Salary']:,.0f} | {m['Bonus %']}%")

    header("4. GroupBy Aggregations")
    teams = {}
    for r in rows:
        t = r["Team"]
        if t not in teams:
            teams[t] = []
        teams[t].append(r["Salary"])
    
    print("Departmental Compensation Summary:")
    print(f"  {'Team':22s} | {'Headcount':9s} | {'Average Salary':14s} | {'Max Salary':10s}")
    print("  " + "-" * 65)
    for t, sals in sorted(teams.items()):
        print(f"  {t:22s} | {len(sals):9d} | ${np.mean(sals):13,.2f} | ${np.max(sals):9,.0f}")

if __name__ == "__main__":
    print("Running Demo 2: Data Ingestion & Manipulation...")
    if HAS_PANDAS:
        run_pandas_mode()
    else:
        run_fallback_mode()
    print("\n[SUCCESS] Demo 2 completed cleanly!\n")
