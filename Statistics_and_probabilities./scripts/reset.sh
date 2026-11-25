#!/usr/bin/env bash
# Reset the local class progression and cache
cd "$(dirname "$0")/.."
echo "Resetting Week 2 Day 1 AM state..."
rm -f .class/progress.md
rm -rf __pycache__ .pytest_cache demos/__pycache__ demos/am/__pycache__
echo "Reset complete. Ready for a fresh class run."
