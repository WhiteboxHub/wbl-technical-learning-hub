# Candidate Progress Tracking State: Data Analysis & Visualization

This document tracks a candidate's learning journey, conceptual understanding, lab exercise completion, and exit check evaluation across both core tracks.

---

## 1. Candidate Metadata

- **Candidate Name:** `[Enter Candidate Name]`
- **Cohort / Track:** WBL Agentic AI Engineering - Week 2 AM
- **Assigned Mentor / Instructor:** `[Enter Instructor Name]`
- **Evaluation Date:** `[YYYY-MM-DD]`
- **Overall Status:** `PENDING` (Options: `PENDING` | `IN_PROGRESS` | `PASSED` | `REQUIRES_REVIEW`)

---

## 2. Learning Beat Mastery Checklist

### Part 1: NumPy & Pandas — Working With Data (Tuesday AM)
| Beat | Topic | Self-Assessment (1-5) | Instructor Verification | Notes & Evidence |
| :--- | :--- | :---: | :---: | :--- |
| **Beat 1.1** | NumPy Memory, Strides & Ndarrays | `[ ]` | `PENDING` | Understood C-contiguous buffers, shape changes |
| **Beat 1.2** | Slicing, Views vs Copies & Broadcasting | `[ ]` | `PENDING` | Demonstrated avoiding unintended view mutation |
| **Beat 1.3** | Pandas Series, DataFrames & Multi-Format I/O | `[ ]` | `PENDING` | Loaded CSV, JSON, verified schema and info() |
| **Beat 1.4** | Indexing (`loc` vs `iloc`) & Boolean Filters | `[ ]` | `PENDING` | Executed multi-condition filtering with `&`, `\|` |
| **Beat 1.5** | Data Cleaning, Missing Values & Types | `[ ]` | `PENDING` | Cleaned `employee_data.csv`, imputed nulls |
| **Beat 1.6** | GroupBy, Multi-Aggregations & Pivots | `[ ]` | `PENDING` | Computed department salary summaries with `agg()` |

### Part 2: EDA & Data Visualization (Wednesday AM)
| Beat | Topic | Self-Assessment (1-5) | Instructor Verification | Notes & Evidence |
| :--- | :--- | :---: | :---: | :--- |
| **Beat 2.1** | Detective's Audit: Summary Stats & Spread | `[ ]` | `PENDING` | Analyzed percentiles, IQR, and skewness |
| **Beat 2.2** | Time Series: Resampling & Rolling Windows | `[ ]` | `PENDING` | Built rolling MA on `timeseries_sample.csv` |
| **Beat 2.3** | Matplotlib Anatomy: Figure, Axes & Subplots | `[ ]` | `PENDING` | Created 4-panel multi-chart dashboard |
| **Beat 2.4** | Seaborn: Boxplots & Regression Plots | `[ ]` | `PENDING` | Plotted departmental salary boxplot & regression |
| **Beat 2.5** | Headless Rendering: Non-GUI Pipeline | `[ ]` | `PENDING` | Enforced `matplotlib.use('Agg')` in scripts |

---

## 3. Mandatory Exit Done-Check Questions

To pass the module, the candidate must answer the following 5 questions without reading pre-written answers:

### Question 1: NumPy Memory & Views (Part 1)
> *Explain the difference between `arr[1:4]` and `arr[1:4].copy()`. What happens to the original array if you mutate the slice in both cases, and why does NumPy behave this way?*
- **Candidate Answer:** `[To be recorded by candidate or coach]`
- **Evaluation:** `PENDING` (Complete / Partial / Inadequate)

### Question 2: Indexing (`loc` vs `iloc`) (Part 1)
> *What is the fundamental difference between `df.loc[0:5]` and `df.iloc[0:5]`? Give a scenario where `df.loc[0]` raises a KeyError while `df.iloc[0]` succeeds.*
- **Candidate Answer:** `[To be recorded by candidate or coach]`
- **Evaluation:** `PENDING` (Complete / Partial / Inadequate)

### Question 3: Missing Value Strategy (Part 1)
> *In `employee_data.csv`, the 'Team' column has missing values and 'Salary' has integer values. Why is it dangerous to simply run `df.dropna()` without parameters? What is the recommended cleaning approach for both categorical and numeric fields?*
- **Candidate Answer:** `[To be recorded by candidate or coach]`
- **Evaluation:** `PENDING` (Complete / Partial / Inadequate)

### Question 4: Split-Apply-Combine & Time Series (Parts 1 & 2)
> *Describe what happens under the hood when executing `df.groupby('Team')['Salary'].agg(['mean', 'max'])`. How does frequency resampling (`resample()`) differ from a rolling moving average (`rolling()`) on a DatetimeIndex?*
- **Candidate Answer:** `[To be recorded by candidate or coach]`
- **Evaluation:** `PENDING` (Complete / Partial / Inadequate)

### Question 5: Visualization Roles & Headless Pipelines (Part 2)
> *When would you choose Matplotlib over Seaborn, and vice versa? In an agentic automated pipeline or server backend, why must we explicitly set `matplotlib.use('Agg')`?*
- **Candidate Answer:** `[To be recorded by candidate or coach]`
- **Evaluation:** `PENDING` (Complete / Partial / Inadequate)

---

## 4. Verification Evidence & Lab Submissions

- **Demo 1 Execution Log:** `[ ] Verified locally`
- **Demo 2 Execution Log:** `[ ] Verified locally`
- **Demo 3 Execution Log:** `[ ] Verified locally (charts generated in demos/output/)`
- **Independent Lab Script:** `[ ] candidate_solution.py created and tested`

---

## 5. Instructor Sign-off
- **Instructor Signature:** `___________________________`
- **Date Signed:** `___________________________`
- **Final Recommendation:** `[RECOMMENDED FOR ADVANCED ML / NEEDS RE-SESSION]`
