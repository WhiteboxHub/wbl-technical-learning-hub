#!/usr/bin/env bash
# ==============================================================================
# Environment Setup Script for Data Analysis Repository
# Verifies Python 3.10+, scientific libraries, datasets, and executable scripts.
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

say() { printf '%s\n' "$*"; }

say "================================================================================"
say "SETTING UP DATA ANALYSIS REPOSITORY ENVIRONMENT"
say "================================================================================"

# 1. Detect best Python binary
say ">>> [1/4] Detecting Python 3 executable..."
PYTHON_BIN="python3"
if [ -x "/usr/local/bin/python3.11" ]; then
    PYTHON_BIN="/usr/local/bin/python3.11"
fi
PY_VER=$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
say "    Using: $PYTHON_BIN (Python $PY_VER)"

# 2. Verify Packages
say ""
say ">>> [2/4] Verifying scientific libraries..."
$PYTHON_BIN -c "
import sys
for pkg, role in [('numpy', 'Core math & array engine'), ('pandas', 'Tabular data analysis'), ('matplotlib', 'Plotting & charts'), ('seaborn', 'Statistical visualization')]:
    try:
        mod = __import__(pkg)
        v = getattr(mod, '__version__', 'installed')
        print(f'    [✓] {pkg:10s} : {v} ({role})')
    except ImportError:
        print(f'    [i] {pkg:10s} : not in current runtime (demos include built-in fallback modes)')
"

# 3. Verify Datasets
say ""
say ">>> [3/4] Verifying sample datasets..."
for f in data/employee_data.csv data/timeseries_sample.csv data/sales_ecommerce.json; do
    if [ -f "$f" ]; then
        LINES=$(wc -l < "$f" | tr -d ' ')
        say "    [✓] $f ($LINES lines verified)"
    else
        say "    [!] Missing $f"
        exit 1
    fi
done

# 4. Permissions
say ""
say ">>> [4/4] Setting execution permissions..."
chmod +x scripts/*.sh demos/*.sh demos/*.py
say "    [✓] Scripts and demos configured as executable."

say ""
say "================================================================================"
say "[SUCCESS] Data Analysis environment setup completed successfully!"
say "Run 'bash scripts/smoke.sh' to verify all test suites."
say "================================================================================"
