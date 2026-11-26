#!/usr/bin/env bash
# Module 2 Lab: Permissions (rwx / Octal), grep, Regex, Pipes & Redirection
# Predict the exact line/row count BEFORE running each search!

# 1. Try executing `/workspace/training_lab/bin/onboarding_helper.sh` as devuser (observe Permission denied),
#    inspect its `ls -l` string, fix permissions with `chmod 755`, run it again, then reset to `chmod 644`:


# 2. Count total lines in `/workspace/training_lab/logs/app.log` (Expected: 120) and count `ERROR` lines (Expected: 15):


# 3. Use Extended Regex (`grep -E`) to show lines matching `ERROR` OR `FATAL` in `logs/app.log` (Expected count: 20):


# 4. From `/workspace/training_lab/logs/auth.log`, extract the top failing IP addresses using a 3-command pipe
#    (`grep` -> `awk` or `cut` -> `sort | uniq -c | sort -nr`):


# 5. Redirect only `FATAL` lines from `logs/app.log` into `/workspace/training_lab/tmp/fatal_only.log`, verify line count (5), then remove it:
