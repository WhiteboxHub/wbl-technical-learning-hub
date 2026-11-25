# Course Table of Contents & Curriculum Map

## Module: Data Analysis (NumPy, Pandas, Cleaning, Timeseries, Visualization)

```
Data Analysis Curriculum Map
├── Act I: The Big Picture (Prologue)
│   ├── Why pure Python fails at scale (Boxed objects vs Contiguous memory)
│   ├── The Workshop Metaphor (NumPy as power tool, Pandas as workbench)
│   └── The Detective's First Walk (Look at data before theorizing)
│
├── Act II: The 7 Core Beats
│   ├── Beat 1: NumPy Memory Architecture, Strides & Ndarrays
│   │   ├── Memory buffers, C-contiguous layout
│   │   ├── Shapes, dimensions (1D, 2D, 3D), and dtypes
│   │   └── Strides and zero-copy reshaping
│   │
│   ├── Beat 2: Slicing Mechanics, The View Trap & Broadcasting
│   │   ├── Slicing syntax [start:stop:step]
│   │   ├── The View vs Copy trap and memory safety
│   │   ├── Broadcasting rules across mismatched dimensions
│   │   └── Vectorized operations vs Python loops benchmark
│   │
│   ├── Beat 3: Pandas Core Architecture & Multi-Format Ingestion
│   │   ├── Series (labeled 1D array) vs DataFrame (aligned 2D table)
│   │   ├── Multi-format readers: CSV, JSON, Excel, SQL, Parquet
│   │   └── Initial data audit: head, tail, info, describe
│   │
│   ├── Beat 4: Indexing (loc vs iloc) & Boolean Filtering
│   │   ├── Integer positional indexing (iloc) vs Label/condition indexing (loc)
│   │   ├── Multi-condition boolean filters (&, |, ~) and operator precedence
│   │   └── String pattern matching (str.contains, isin)
│   │
│   ├── Beat 5: Data Cleaning, Missing Values & Type Casting
│   │   ├── Diagnosing null patterns (isna().sum())
│   │   ├── Imputation strategies (fillna with constants, mean, median)
│   │   ├── Pruning policies (dropna how='all' vs subset)
│   │   └── Safe type casting (astype, to_datetime)
│   │
│   ├── Beat 6: Split-Apply-Combine Aggregations & Pivot Tables
│   │   ├── The Split-Apply-Combine mental model
│   │   ├── Multi-metric aggregation with .agg()
│   │   ├── Pivot tables and multi-dimensional cross-tabulations
│   │   └── Sorting and merging datasets
│   │
│   └── Beat 7: Time Series & Dual Visualization (Matplotlib + Seaborn)
│       ├── DatetimeIndex, frequency resampling ('D', 'W', 'M')
│       ├── Rolling window moving averages (trend smoothing)
│       ├── Matplotlib: Figure/Axes anatomy, subplots, line/bar/hist
│       ├── Seaborn: Statistical aesthetics, boxplots, regression plots
│       └── Headless rendering with matplotlib.use('Agg')
│
└── Act III: Synthesis, Lab Verification & Exit Checks (Epilogue)
    ├── End-to-end smoke tests and automated verification
    ├── 5 Mandatory Done-Check Exit Questions
    └── candidate-state.md sign-off
```

