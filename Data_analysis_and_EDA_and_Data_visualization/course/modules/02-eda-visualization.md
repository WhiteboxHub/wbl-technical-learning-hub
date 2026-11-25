# Part 2: EDA + Data Visualization (Wednesday AM)

**Track Name:** `[PART-2: EDA & DATA VISUALIZATION]`  
**Curriculum Alignment:** WBL Agentic AI Engineering, Week 2 Wednesday AM  
**Story Anchor:** *The Detective's First Walk: The detective's first walk through the crime scene — look before you theorise.*

---

## Act I: Tell Them What You Are Going to Tell Them (The Big Picture)

### The Opening Hook
In machine learning and agentic analytics, raw numbers in tables can hide deceptive traps: Simpson's paradox, severe skewness, bimodal clusters, or subtle anomalies. Before any feature engineering or hypothesis testing occurs, we must behave like a detective arriving at a crime scene: **look before you theorise**.

Today, we learn Exploratory Data Analysis (EDA) and Visualization:
- **Exploratory Data Analysis (EDA)** is the systematic interrogation of distributions, central tendencies, outliers, and relationships.
- **Matplotlib** gives us surgical, low-level control over the canvas, subplots, coordinates, and rendering pipelines.
- **Seaborn** gives us statistical elegance: automated regression estimates, confidence intervals, distribution plots, and categorical insights.

---

## Act II: Tell Them (Core Beats for Part 2)

### Beat 2.1: The Detective's Audit — Summary Statistics & Distributions
- **Cue:** Open `demos/demo3_timeseries_and_visualization.py` and inspect data statistics.
- **Say:** "A single metric like the mean can lie. If Elon Musk walks into a room of 10 people, the average net worth is over \$20 billion, but 10 people are still living on ordinary salaries. EDA begins by checking the spread: percentiles (25%, 50%, 75%), IQR, min, max, and skewness."
- **Key Concepts:**
  - `df.describe()`: 5-number summary across numeric columns.
  - Parametric (Mean, Standard Deviation) vs Non-Parametric (Median, IQR).
  - Skewness: Right-skewed (tail on right, mean > median) vs Left-skewed.
- **Ask:** *"If salary data has mean \$95,000 and median \$64,000, what does this tell the detective about the organization?"*
- **Answer:** The distribution is strongly right-skewed; a few top executives pull the arithmetic mean upward, while most employees earn around \$64,000.

---

### Beat 2.2: Time Series Ingestion, Frequency Resampling & Rolling Windows
- **Cue:** Run section 1 of Demo 3 on `data/timeseries_sample.csv`.
- **Say:** "Data points separated by time are not independent; they have temporal structure. By turning dates into a `DatetimeIndex`, Pandas unlocks calendar frequencies and trend smoothing."
- **Key Concepts:**
  - `pd.to_datetime()` & `df.set_index('Date')`.
  - Frequency Resampling: `df['Revenue'].resample('W').sum()` or `'3D'`.
  - Rolling Windows: `df['Revenue'].rolling(window=7).mean()` (removes daily noise to reveal underlying trajectory).
- **Ask:** *"What is the difference between resample() and rolling()?"*
- **Answer:** `resample()` changes the frequency and shrinks the number of rows (like GroupBy for time). `rolling()` keeps the original row count, computing a moving window calculation for each timestamp.

---

### Beat 2.3: Matplotlib Anatomy & The Figure/Axes Hierarchy
- **Cue:** Display the 4-panel dashboard generation in Demo 3.
- **Say:** "Many developers use `plt.plot()` blindly and get confused when multiple charts collide. Professional data scientists use the Object-Oriented interface: `fig, ax = plt.subplots()`."
- **Key Concepts:**
  - **Figure:** The overall canvas window.
  - **Axes:** The actual individual plot/chart with x-axis, y-axis, labels, and ticks.
  - Anatomy of a Plot: Title, X/Y labels, grid, legend, tick formatters, and annotations.
  - Chart Types:
    - Line chart: Trends over time.
    - Bar chart: Categorical comparisons.
    - Histogram: Distribution and bin frequency.
    - Scatter plot: Relationships between two continuous variables (with optional color hue).
- **Ask:** *"Why do we use fig, axes = plt.subplots(2, 2) instead of calling plt.subplot() four times?"*
- **Answer:** `plt.subplots()` returns an array of axes objects that can be referenced explicitly (e.g. `axes[0, 1]`), making code modular, readable, and reproducible in automated scripts.

---

### Beat 2.4: Seaborn Statistical Visualizations (Boxplots & Regressions)
- **Cue:** Display the Seaborn statistical analysis in Demo 3 (`seaborn_statistical_plots.png`).
- **Say:** "Matplotlib gives you bricks and mortar; Seaborn gives you an architect-designed home. Seaborn is built directly on top of Pandas and Matplotlib, automating statistical calculations like confidence intervals and distribution curves."
- **Key Concepts:**
  - Statistical Styling: `sns.set_theme(style='whitegrid')`.
  - `sns.boxplot()`: Displays median, quartiles (Q1, Q3), whiskers (1.5 * IQR), and outlier dots.
  - `sns.regplot()` / `sns.lmplot()`: Computes linear regression trendlines with shaded 95% bootstrap confidence bands.
  - `hue` parameter: Instantly segments data by categorical groups (e.g. Gender, Team, Store).
- **Ask:** *"How does a boxplot define an outlier mathematically?"*
- **Answer:** Any point falling below $Q_1 - 1.5 \times \text{IQR}$ or above $Q_3 + 1.5 \times \text{IQR}$, where $\text{IQR} = Q_3 - Q_1$.

---

### Beat 2.5: The Headless Pipeline Imperative (`matplotlib.use('Agg')`)
- **Cue:** Show the import block of Demo 3.
- **Say:** "When running AI agents, CI/CD pipelines, or Docker containers, there is no physical monitor attached. If code calls `plt.show()`, the script crashes or hangs indefinitely."
- **The Rule:**
  ```python
  import matplotlib
  matplotlib.use('Agg')  # Headless non-GUI raster backend
  import matplotlib.pyplot as plt
  ```
  Always save charts to files (`demos/output/my_chart.png`) instead of calling `plt.show()`.

---

## Act III: Tell Them What You Told Them (Part 2 Synthesis)

1. **Look Before You Theorise:** Use summary statistics and distributions to spot skewness and outliers before modeling.
2. **Smooth the Trend:** Use `DatetimeIndex`, frequency resampling, and rolling averages to uncover temporal signal from noise.
3. **Master the Canvas:** Use Matplotlib's Object-Oriented `fig, ax` interface for custom multi-panel layouts.
4. **Harness Statistical Elegance:** Use Seaborn for boxplots, regression trendlines, and grouped categorical analysis.
5. **Never Crash the Pipeline:** Always enforce `matplotlib.use('Agg')` in agentic and server environments.

