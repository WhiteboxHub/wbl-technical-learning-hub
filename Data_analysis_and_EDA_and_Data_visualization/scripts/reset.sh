#!/usr/bin/env bash
# ==============================================================================
# Reset Script: Cleans up generated demo outputs, caches, and progress tracking
# ==============================================================================
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "================================================================================"
echo "RESETTING DATA ANALYSIS REPOSITORY ARTIFACTS"
echo "================================================================================"

# Remove generated plots
if [ -d "demos/output" ]; then
    rm -f demos/output/*.png demos/output/*.svg
    echo "  [OK] Cleaned demos/output/"
fi

# Remove python caches
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "  [OK] Removed Python bytecode and cache files."

# Reset .class/progress.md beat tracker if present
cat << 'EOF' > .class/progress.md
# In-Class Beat Tracking Log

| Beat | Topic | Status | Timestamp | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Beat 1 | NumPy Memory Layout, Strides & Arrays | PENDING | - | Initial state |
| Beat 2 | Slicing, Copy vs View & Vectorization | PENDING | - | Initial state |
| Beat 3 | Pandas Series, DataFrames & Multi-format I/O | PENDING | - | Initial state |
| Beat 4 | Indexing (loc vs iloc) & Boolean Filtering | PENDING | - | Initial state |
| Beat 5 | Data Cleaning: Missing Values & Transformations | PENDING | - | Initial state |
| Beat 6 | GroupBy, Aggregations & Pivot Tables | PENDING | - | Initial state |
| Beat 7 | Time Series & Dual Visualization (Matplotlib + Seaborn) | PENDING | - | Initial state |
EOF
echo "  [OK] Reset .class/progress.md to initial state."

echo ""
echo "[RESET COMPLETE] The repository is clean and reset to starting baseline."

