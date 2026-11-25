# Student Study Guide & Lab Workbook: Data Analysis

Welcome to the Data Analysis module of the WBL Agentic AI Engineering Program!

---

## 1. Core Mental Models & Cheatsheets

### Mental Model 1: NumPy Memory & Strides
A NumPy array (`ndarray`) is stored as a contiguous memory block in RAM:
```
Memory Address: [ 0x1000 ][ 0x1004 ][ 0x1008 ][ 0x100C ][ 0x1010 ][ 0x1014 ]
Values:         [   10   ][   20   ][   30   ][   40   ][   50   ][   60   ]
```
If shaped as `(2, 3)` with 4-byte integers:
- Shape: `(2, 3)`
- Strides: `(12, 4)` -> Step 12 bytes to move down 1 row (3 elements $\times$ 4 bytes); step 4 bytes to move 1 column.

### Mental Model 2: The View vs Copy Rule
- **Slice (`a[1:4]`):** Returns a **VIEW**. Shares the same memory. Changing elements in the slice changes the original array!
- **Explicit Copy (`a[1:4].copy()`):** Allocates a brand-new memory buffer. Completely independent.

### Mental Model 3: Indexing in Pandas
| Operator | Type | Coordinate System | Stop Index |
| :--- | :--- | :--- | :--- |
| `df.iloc[row_idx, col_idx]` | Positional | 0 to N-1 (integers only) | **Exclusive** (`0:3` gets 0, 1, 2) |
| `df.loc[row_lbl, col_lbl]` | Label / Condition | Index labels & column names | **Inclusive** (`0:3` gets 0, 1, 2, 3) |

---

## 2. Hands-on Lab Exercises (Practice with Repository Data)

### Exercise 1: NumPy Array Manipulation
Create a Python script or notebook that:
1. Creates a 2D array of shape `(5, 5)` filled with integers from 1 to 25.
2. Extracts the inner `3x3` matrix using slicing.
3. Replaces all even numbers in the inner matrix with `-1` without modifying the original outer border.
4. *Hint:* Remember to check whether your slice is a view or an explicit copy!

### Exercise 2: Cleaning `data/employee_data.csv`
Load `data/employee_data.csv` using Pandas:
1. Print the count of missing values per column.
2. Impute missing values:
   - 'First Name' -> `"Unknown"`
   - 'Gender' -> `"Unspecified"`
   - 'Team' -> `"General Pool"`
3. Convert 'Start Date' to a datetime object.
4. Calculate the average salary for each 'Team', sorted in descending order.

### Exercise 3: Time Series Analysis with `data/timeseries_sample.csv`
1. Load `data/timeseries_sample.csv` and set the 'Date' column as the `DatetimeIndex`.
2. Compute the 7-day rolling average of 'Revenue'.
3. Find the store region that generated the highest total revenue.

### Exercise 4: Visualizing with Matplotlib & Seaborn
1. Load `data/employee_data.csv`.
2. Create a 2-panel figure:
   - Panel 1 (Matplotlib): Histogram of 'Salary' with 10 bins.
   - Panel 2 (Seaborn): Boxplot comparing 'Salary' distributions across 'Gender'.
3. Save the resulting figure to `demos/output/my_practice_plot.png`.

---

## 3. Self-Study Exit Check Questions
Test your readiness by answering the 5 Done-Check questions in `candidate-state.md`. When ready, request an assessment from your instructor or practice coach agent.

