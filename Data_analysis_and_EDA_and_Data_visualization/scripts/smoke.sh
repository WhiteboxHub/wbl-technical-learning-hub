#!/usr/bin/env bash
# ==============================================================================
# Smoke Test Script for Data Analysis Repository
# Verifies datasets, imports, and executes all test suites without failure.
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

say() { printf '%s\n' "$*"; }

say "================================================================================"
say "RUNNING DATA ANALYSIS SMOKE TEST SUITE"
say "================================================================================"

# Pick best python binary
PYTHON_BIN="python3"
if [ -x "/usr/local/bin/python3.11" ]; then
    PYTHON_BIN="/usr/local/bin/python3.11"
fi

# 1. Package Verification
say "1. Testing Python packages..."
$PYTHON_BIN -c "
import sys
try:
    import numpy as np
    print(f'   [✓] numpy: {np.__version__} (Core array engine)')
except ImportError:
    print('   [!] ERROR: numpy is required.')
    sys.exit(1)

for p in ['pandas', 'matplotlib', 'seaborn']:
    try:
        mod = __import__(p)
        print(f'   [✓] {p}: {getattr(mod, \"__version__\", \"installed\")}')
    except ImportError:
        print(f'   [i] {p}: optional package (demos use robust built-in fallbacks)')
"

# 2. Check Datasets
say "2. Testing sample datasets..."
test -f data/employee_data.csv && say "   [✓] data/employee_data.csv verified."
test -f data/timeseries_sample.csv && say "   [✓] data/timeseries_sample.csv verified."
test -f data/sales_ecommerce.json && say "   [✓] data/sales_ecommerce.json verified."

# 3. Run All Demos
say "3. Testing Data Analysis Demos..."
$PYTHON_BIN demos/demo1_numpy_speed_and_broadcasting.py > /dev/null
say "   [✓] Demo 1 (NumPy Vectorization, Strides & Broadcasting) ran successfully."

$PYTHON_BIN demos/demo2_pandas_cleaning_and_aggregation.py > /dev/null
say "   [✓] Demo 2 (Pandas Ingestion, Cleaning & Aggregation) ran successfully."

$PYTHON_BIN demos/demo3_timeseries_and_visualization.py > /dev/null
say "   [✓] Demo 3 (Timeseries & Dual Visualizations) ran successfully."

# 4. Check Generated Output
test -f demos/output/matplotlib_dashboard.png && say "   [✓] Output: demos/output/matplotlib_dashboard.png verified."
test -f demos/output/seaborn_statistical_plots.png && say "   [✓] Output: demos/output/seaborn_statistical_plots.png verified."

say ""
say "================================================================================"
say "ALL DATA ANALYSIS SMOKE TESTS PASSED SUCCESSFULLY!"
say "================================================================================"
exit 0
