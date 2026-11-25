#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PYTHON_BIN="python3"
if [ -x "/usr/local/bin/python3.11" ]; then
    PYTHON_BIN="/usr/local/bin/python3.11"
fi

echo "================================================================================"
echo "RUNNING ALL DATA ANALYSIS DEMOS (NUMPY, PANDAS, TIMESERIES & DATA VIZ)"
echo "Using Python: $PYTHON_BIN"
echo "================================================================================"

echo ""
echo ">>> [1/3] Executing Demo 1: NumPy Vectorization, Strides & Broadcasting..."
$PYTHON_BIN demo1_numpy_speed_and_broadcasting.py

echo ""
echo ">>> [2/3] Executing Demo 2: Pandas Ingestion, Missing Data & Aggregations..."
$PYTHON_BIN demo2_pandas_cleaning_and_aggregation.py

echo ""
echo ">>> [3/3] Executing Demo 3: Timeseries, Matplotlib Dashboard & Seaborn Plots..."
$PYTHON_BIN demo3_timeseries_and_visualization.py

echo ""
echo "================================================================================"
echo "ALL DEMOS EXECUTED SUCCESSFULLY!"
echo "Check generated charts in: demos/output/"
echo "================================================================================"
