# Part 1: NumPy & Pandas — Working With Data (Tuesday AM)

**Track Name:** `[PART-1: NUMPY & PANDAS]`  
**Curriculum Alignment:** WBL Agentic AI Engineering, Week 2 Tuesday AM  
**Story Anchor:** *The Workshop: NumPy is the power tool, Pandas is the workbench with labelled drawers.*

---

## Act I: Tell Them What You Are Going to Tell Them (The Big Picture)

### The Opening Hook
Every modern machine learning model, embedding pipeline, and agentic reasoning workflow is fundamentally fed by tabular and numeric data. Before an agent can analyze an invoice, predict user churn, or compute vector cosine similarity, raw data must be loaded, sanitized, sliced, and transformed.

Python by itself is slow for numeric processing because every Python integer is a boxed C struct requiring 28 bytes of heap memory and dynamic pointer chasing. Today, we step into the workshop:
- **NumPy** is our raw industrial power tool: dense contiguous C-arrays, SIMD vectorization, memory strides, and broadcasting.
- **Pandas** is our organized workbench: labeled drawers (column names), structured indices, multi-format I/O, and SQL-like grouping.

---

## Act II: Tell Them (Core Beats for Part 1)

### Beat 1.1: NumPy Memory Architecture, Strides & Ndarrays
- **Cue:** Open `demos/demo1_numpy_speed_and_broadcasting.py`.
- **Say:** "A Python list of integers is not an array of numbers; it is an array of pointers pointing to integers scattered across memory. When you loop over a Python list, the CPU cache misses constantly. A NumPy `ndarray` is a single contiguous block of raw bytes in memory. The array's header stores its `shape`, `dtype`, and `strides`."
- **Demo:** Run benchmark and stride exploration in Demo 1.
- **Key Concepts:**
  - `np.ndarray`: Contiguous memory buffer + shape/dtype metadata.
  - `strides`: The number of bytes to step in memory to advance one element along each dimension.
  - `itemsize`: Byte size of a single element (e.g. `int32` = 4 bytes, `float64` = 8 bytes).
  - Reshaping changes metadata only; it does not duplicate underlying bytes.
- **Ask:** *"If you reshape a 1D array of 12 elements into a 3x4 2D array of 4-byte integers, what are the strides of the resulting array?"*
- **Answer:** `(16, 4)`. Skipping one row requires advancing 4 elements $\times$ 4 bytes = 16 bytes. Skipping one column requires 4 bytes.

---

### Beat 1.2: Slicing Mechanics, The View Trap & Broadcasting
- **Cue:** Display section 3 and 4 of Demo 1.
- **Say:** "In standard Python, slicing a list creates a brand new copy: `b = a[:]`. In NumPy, slicing returns a **VIEW** that points to the exact same memory buffer. If you modify the view, you silently mutate the parent array! To get an independent copy, you must explicitly call `.copy()`."
- **Demo:** Show mutating a slice vs an explicit copy.
- **Broadcasting Rules:**
  When operating on two arrays, NumPy compares their shapes element-wise from right to left (trailing dimensions first):
  1. Dimensions are compatible if they are equal, OR
  2. One of the dimensions is 1.
  If dimension is 1, it is virtually stretched across the other array without copying memory.
- **Ask:** *"Can an array of shape (4, 1, 6) be broadcast with an array of shape (3, 6)? What is the resulting shape?"*
- **Answer:** Yes. Trailing dimension 6 matches 6. Next dimension 1 matches 3 (stretched to 3). Leading dimension 4 matches implicit 1 (stretched to 4). Resulting shape is `(4, 3, 6)`.

---

### Beat 1.3: Pandas Architecture & Multi-Format Ingestion
- **Cue:** Open `demos/demo2_pandas_cleaning_and_aggregation.py` and inspect `data/employee_data.csv`.
- **Say:** "NumPy gave us raw speed, but the real world has column names, missing data, and mixed types. Pandas is our workbench. A `Series` is a labeled 1D array. A `DataFrame` is an aligned table of Series sharing an index."
- **Demo:** Load CSV, JSON, and inspect data types with `df.info()`.
- **Supported Formats:**
  - `pd.read_csv()`: Tabular comma-delimited data.
  - `pd.read_json()`: Nested or flat JSON payloads.
  - `pd.read_excel()`: Multi-sheet spreadsheet files.
  - `pd.read_sql()`: Relational database queries.
  - `pd.read_parquet()`: Compressed columnar storage for big data.
- **Ask:** *"Why does df.info() say an entire column is 'object' dtype when it only contains strings or mixed nulls?"*
- **Answer:** Pandas traditionally represents string and mixed columns as generic Python pointer objects. In modern Pandas, specifying `dtype="string"` or `string[pyarrow]` yields true typed arrow arrays with immense memory savings.

---

### Beat 1.4: Indexing (`loc` vs `iloc`) & Complex Boolean Filtering
- **Cue:** Open section 3 and 4 of Demo 2.
- **Say:** "The number one source of confusion in Pandas is `loc` versus `iloc`. Remember this rule: `iloc` is integer position only, exactly like Python list indexing (0 to N-1, exclusive of stop). `loc` is label-based and boolean condition-based (and its stop slice is INCLUSIVE!)."
- **Demo:** Run comparisons of `df.iloc[0:3, 0:2]` vs `df.loc[0:3, ['Salary', 'Team']]`.
- **Boolean Logic in Pandas:**
  - Python's `and`, `or`, `not` keywords do NOT work across vector series.
  - Always use bitwise operators: `&` (AND), `|` (OR), `~` (NOT), wrapped in parentheses.
  - Example: `df[(df['Salary'] > 90000) & (df['Team'] == 'Marketing')]`.
- **Ask:** *"Why must we wrap each condition in parentheses when filtering with `&` in Pandas?"*
- **Answer:** In Python operator precedence, bitwise `&` has higher precedence than comparison operators like `>`. Without parentheses, `df['Salary'] > 90000 & df['Team'] == 'Marketing'` evaluates `90000 & df['Team']` first, causing a `TypeError`.

---

### Beat 1.5: Data Cleaning, Missing Values & Type Casting
- **Cue:** Inspect null values in `employee_data.csv`.
- **Say:** "Real-world data is dirty. Missing values, wrong dates, string booleans. Our job as data detectives is to audit before we train."
- **Demo:**
  ```python
  # Diagnose
  df.isna().sum()
  
  # Impute
  df['Team'] = df['Team'].fillna('Unassigned')
  
  # Cast
  df['Start Date'] = pd.to_datetime(df['Start Date'])
  df['Senior Management'] = df['Senior Management'].astype('boolean')
  ```
- **Pruning vs Imputation:**
  - `dropna(how='all')`: Drop only rows where every single column is null.
  - `dropna(subset=['Critical_Column'])`: Drop rows only if the specific required identifier is missing.
  - `fillna(value)` or `fillna(method='ffill')`: Impute forward or with constants/medians.
- **Ask:** *"When should you fill missing values with the median instead of the mean?"*
- **Answer:** When the column contains extreme outliers or skewed distributions (e.g., compensation or house prices), because the median is robust to extreme values whereas the mean gets distorted.

---

### Beat 1.6: Split-Apply-Combine Aggregations & Pivot Tables
- **Cue:** Run GroupBy section of Demo 2.
- **Say:** "Hadley Wickham coined the universal data pattern: Split-Apply-Combine. In Pandas, `df.groupby('Team')` splits the DataFrame into distinct departmental groups, applies aggregation functions (`mean`, `sum`, `count`), and combines them into a summary."
- **Demo:** Run multi-metric aggregation:
  ```python
  df.groupby('Team').agg(
      headcount=('Salary', 'count'),
      avg_salary=('Salary', 'mean'),
      max_salary=('Salary', 'max')
  )
  ```
- **Pivot Tables:** `pd.pivot_table()` creates multidimensional summaries with row indices, column headers, and aggregation values.
- **Ask:** *"What is the difference between df.groupby('Team').mean() and df.groupby('Team')[['Salary']].mean()?"*
- **Answer:** The first attempts to compute the mean across *all* columns in the DataFrame (failing or warning if there are non-numeric string columns). The second slices the numeric `'Salary'` column first, computing the mean safely and efficiently.

---

## Act III: Tell Them What You Told Them (Part 1 Synthesis)

1. **NumPy is the Engine:** Contiguous memory, fixed types, strides, and SIMD vectorization make NumPy orders of magnitude faster than pure Python loops.
2. **Beware the View Trap:** Slicing creates views that share memory; use `.copy()` when you need isolated mutation.
3. **Pandas is the Workbench:** Use `loc` for labels and boolean conditions, `iloc` for integer coordinates. Always wrap boolean conditions in parentheses `(cond1) & (cond2)`.
4. **Clean Before You Compute:** Audit nulls with `.isna().sum()`, convert dates with `pd.to_datetime()`, and impute with domain awareness.
5. **Next Step:** Now that our data is clean, we move to **Part 2: EDA + Data Visualization** to explore distributions, correlations, and tell visual stories.

