#!/usr/bin/env bash
# Module 1 Reference Solutions (Instructors & Post-Attempt Verification Only)
set -e
cd /workspace/training_lab

# 1. Kernel, user, working directory
uname -s
whoami
pwd

# 2. Case-sensitivity check (Report.txt vs report.txt)
ls -la /workspace/training_lab/docs
head -n 2 docs/Report.txt docs/report.txt

# 3. Relative navigation from logs/
(cd /workspace/training_lab/logs && head -n 3 ../docs/readme.txt)

# 4. Absolute path inspection + temp dir create & cleanup
grep '^devuser:' /etc/passwd
mkdir -p /workspace/training_lab/tmp/notes
echo "Unix paths start at root /" > /workspace/training_lab/tmp/notes/day1.txt
cat /workspace/training_lab/tmp/notes/day1.txt
rm -rf /workspace/training_lab/tmp/notes
