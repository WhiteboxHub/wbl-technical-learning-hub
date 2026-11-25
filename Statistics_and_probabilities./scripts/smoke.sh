#!/usr/bin/env bash
# Smoke test verifying Week 2 Day 1 AM environment, datasets, and demos
set -euo pipefail
cd "$(dirname "$0")/.."

say() { printf '%s\n' "$*"; }

say "Running smoke tests for Week 2 Day 1 AM (Statistics & Probability for ML)..."

# 1. Package import verification
say "1. Testing Python packages..."
python3 -c "
import sys
try:
    import numpy as np
    print(f'   [✓] numpy: {np.__version__} (Core math engine)')
except ImportError:
    print('   [!] ERROR: numpy is required. Install via pip install numpy')
    sys.exit(1)

optional = ['scipy', 'matplotlib', 'pandas']
for p in optional:
    try:
        mod = __import__(p)
        print(f'   [✓] {p}: {getattr(mod, \"__version__\", \"installed\")}')
    except ImportError:
        print(f'   [i] {p}: optional package not installed (demos use robust built-in fallbacks)')
"

# 2. Check datasets
say "2. Testing sample datasets..."
test -f data/medical_screening_sample.csv && say "   [✓] data/medical_screening_sample.csv verified."
test -f data/weather_forecaster_survey.csv && say "   [✓] data/weather_forecaster_survey.csv verified."

# 3. Check AM Demos
say "3. Testing Statistics Demos..."
python3 demos/demo1_distributions.py --samples 500 > /dev/null
say "   [✓] Demo 1 (Distributions, Skewness, Spread) ran successfully."

python3 demos/demo2_bayes_calculator.py --prevalence 0.01 --sensitivity 0.95 --fp-rate 0.05 > /dev/null
say "   [✓] Demo 2 (Bayes Calculator & Natural Frequencies) ran successfully."

python3 demos/demo3_sampling_bias.py > /dev/null
say "   [✓] Demo 3 (Sampling Bias & Signal vs Noise) ran successfully."

say "\nAll Week 2 Day 1 AM smoke tests passed successfully!"
exit 0
