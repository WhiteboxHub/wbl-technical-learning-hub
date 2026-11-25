#!/usr/bin/env bash
# ==============================================================================
# Helper to execute any python script using the repository's configured Python
# ==============================================================================
if [ -x "/usr/local/bin/python3.11" ]; then
    EXEC_PY="/usr/local/bin/python3.11"
elif command -v python3 &>/dev/null; then
    EXEC_PY="python3"
else
    echo "No python3 found."
    exit 1
fi

exec "$EXEC_PY" "$@"

