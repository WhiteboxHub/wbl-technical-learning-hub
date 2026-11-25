#!/usr/bin/env bash
# One-command setup for Week 2 Day 1 AM: Statistics & Probability for ML
#   scripts/setup.sh           check prerequisites, install packages, verify demos, run smoke test
#   scripts/setup.sh --reset   clean progress and generated test artifacts
#
# Exit codes: 0 ok | 10 python missing | 11 python version < 3.10
#             13 install failed | 14 smoke test failed
set -euo pipefail
cd "$(dirname "$0")/.."

say()  { printf '%s\n' "$*"; }
step() { printf '\n== %s\n' "$*"; }

if [ "${1:-}" = "--reset" ]; then
  step "Resetting class progression and cache"
  rm -f .class/progress.md
  rm -rf __pycache__ .pytest_cache demos/__pycache__ demos/am/__pycache__
  say "Reset complete."
  exit 0
fi

step "Checking prerequisites"
command -v python3 >/dev/null 2>&1 || { say "ERROR: python3 not found. Install Python 3.10+"; exit 10; }

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
  say "ERROR: Python 3.10 or higher required. Found Python $PY_VER"; exit 11;
fi
say "python3 ($PY_VER) ok"

step "Checking Python virtual environment"
if [ ! -d ".venv" ]; then
  say "Creating virtual environment in .venv..."
  python3 -m venv .venv
fi
if [ -f ".venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
  say "Activated virtual environment (.venv)"
fi

step "Verifying packages from requirements.txt"
python3 -c "import numpy, pandas, scipy, matplotlib; print('Installed packages verified.')" >/dev/null 2>&1 || {
  say "Installing/updating dependencies..."
  pip install -q -r requirements.txt || { say "ERROR: pip install failed."; exit 13; }
}
say "Python packages: numpy, pandas, scipy, matplotlib all verified."

step "Verifying starter datasets"
test -f data/medical_screening_sample.csv || { say "ERROR: Missing data/medical_screening_sample.csv"; exit 14; }
test -f data/weather_forecaster_survey.csv || { say "ERROR: Missing data/weather_forecaster_survey.csv"; exit 14; }
say "Datasets verified in data/."

step "Smoke test"
chmod +x scripts/smoke.sh demos/run_all.sh
if scripts/smoke.sh; then
  step "READY"
  say "Environment:     Python $PY_VER (.venv activated)"
  say "Topic:           Week 2 Day 1 AM: Statistics & Probability for ML"
  say "Story Anchor:    The weather forecaster who is never certain, only honest about the odds"
  say "Course Material: course/modules/01-statistics-and-probability.md"
  say "Demos:           demos/ (demo1_distributions.py, demo2_bayes_calculator.py, demo3_sampling_bias.py)"
  say "Runner:          bash demos/run_all.sh"
  say "Multi-Agent:     skills/stats-skill/SKILL.md, AGENTS.md, docs/agent-prompts.md"
  say "Reset Progress:  scripts/setup.sh --reset"
  exit 0
fi

say "ERROR: Smoke test failed. Inspect error logs above."
exit 14
