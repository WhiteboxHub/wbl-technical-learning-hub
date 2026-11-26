#!/usr/bin/env bash
# Module 1 Lab: Unix Architecture, Case Sensitivity, Relative vs Absolute Paths & Safe Navigation
# Start inside /workspace/training_lab (`scripts/sh.sh`)

# 1. Verify OS, current shell, and current working directory
#    - Run uname -a, echo "$SHELL", and pwd

# 2. Case sensitivity test (Slides 16)
#    - List and read both docs/Report.txt and docs/report.txt to prove Unix treats them as two distinct files.

# 3. Relative vs Absolute Paths (Slides 22-25)
#    - cd into docs/
#    - Use a RELATIVE path (`../config/...`) to read config/app.conf
#    - Use an ABSOLUTE path (`/etc/passwd`) to inspect the first 5 lines (`head -n 5 /etc/passwd`)
#    - Return to /workspace/training_lab

# 4. Safe file & directory operations (Slides 18-19)
#    - Create tmp/practice_dir, copy docs/servers.csv inside it, rename it to servers_copy.csv,
#      list it with `ls -l`, then remove tmp/practice_dir cleanly (`rm -r`).
