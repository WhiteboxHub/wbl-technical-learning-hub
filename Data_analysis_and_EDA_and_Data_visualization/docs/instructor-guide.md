# Comprehensive Instructor Guide: Data Analysis

**Target Level:** Intermediate Python / AI Engineering Candidates  
**Pedagogy:** Socratic Inquiry + WBL Tripartite Structure  
**Story Anchors:**
- *The workshop: NumPy is the power tool, Pandas is the workbench with labelled drawers.*
- *The detective's first walk through the crime scene - look before you theorise.*

---

## 1. Pedagogical Architecture

### Why This Sequence?
1. **NumPy First:** Understanding contiguous memory buffers, shapes, and strides prevents candidates from viewing Pandas as 'magic'. When they understand that a Pandas column is a NumPy array under the hood, operations like vectorization and broadcasting become intuitive.
2. **Pandas Second:** Introduce the workbench: labeled indices, column names, null value management, and relational operations.
3. **Visual EDA Third:** Data visualization is not just pretty charts—it is an investigative step before feature engineering or modeling. We teach dual visualization: Matplotlib for low-level canvas layout and subplots, and Seaborn for high-level statistical summaries.

---

## 2. Common Candidate Pitfalls & How to Address Them

### Pitfall 1: Looping over Pandas DataFrames (`for index, row in df.iterrows()`)
- **Symptom:** Candidates write Python for-loops to transform column values.
- **The Intervention:** "In Python, looping over 100,000 rows takes seconds because you are instantiating 100,000 Series objects. Vectorization executes in C SIMD registers in 2 milliseconds. Never loop over a DataFrame unless an operation is strictly sequential."

### Pitfall 2: The `SettingWithCopyWarning` Trap
- **Symptom:** Candidates execute `df[df['Salary'] > 50000]['Bonus'] = 10` and receive a warning.
- **The Intervention:** Explain the difference between chained indexing and `.loc[]`. Chained indexing creates an ambiguous intermediate object. Always write:
  ```python
  df.loc[df['Salary'] > 50000, 'Bonus'] = 10
  ```

### Pitfall 3: Indiscriminate `dropna()`
- **Symptom:** Candidates run `df.dropna(inplace=True)` and wipe out 70% of their dataset.
- **The Intervention:** "Data is expensive. Pruning without checking missing distributions discards valuable signals. Check `df.isna().sum()` first, determine if nulls are MAR (Missing at Random), and impute appropriately."

---

## 3. Exit Check Evaluation Rubric

When evaluating candidates against `candidate-state.md`:

| Mastery Level | Criteria | Action |
| :--- | :--- | :--- |
| **Exemplary (Pass)** | Explains C-contiguous memory, views vs copies, `loc` vs `iloc` mechanics, handles missing data appropriately, and interprets statistical charts cleanly. | Sign off `candidate-state.md` as PASSED. Advance to Machine Learning modules. |
| **Competent (Pass)** | Writes correct Pandas and NumPy code with minor prompting on syntax. Understands why vectorization is fast. | Sign off as PASSED with self-study reading on strides. |
| **Developing (Review)** | Relies on loops, confuses `loc` and `iloc`, fails to recognize view mutation risks. | Assign Lab Exercises 1-4 in `docs/student-guide.md` and re-evaluate. |

