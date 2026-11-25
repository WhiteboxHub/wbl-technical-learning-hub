#!/usr/bin/env bash
set -e

echo "=== ClaimFlow AI Setup ==="

# Check Python
if command -v python3 &>/dev/null; then
    PY_BIN="python3"
elif command -v python &>/dev/null; then
    PY_BIN="python"
else
    echo "Error: Python 3 is not installed."
    exit 1
fi

echo "Using Python: $($PY_BIN --version)"

# Create virtual environment if not present
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    $PY_BIN -m venv .venv
fi

# Activate virtualenv
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

# Install dependencies
pip install -r requirements.txt

echo "Setup completed successfully. Run 'bash scripts/smoke.sh' to verify."
