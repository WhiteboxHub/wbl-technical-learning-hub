#!/usr/bin/env bash
# Module 2 Reference Solutions (Instructors & Post-Attempt Verification Only)
set -e
cd /workspace/training_lab

# 1. Permission fix drill (Expected before: -rw-r--r-- -> Permission denied)
ls -l bin/onboarding_helper.sh
chmod 755 bin/onboarding_helper.sh
./bin/onboarding_helper.sh
chmod 644 bin/onboarding_helper.sh

# 2. Exact log counts (120 total, 15 ERROR)
wc -l logs/app.log
grep -c "ERROR" logs/app.log

# 3. Extended regex ERROR or FATAL (20 lines)
grep -cE "ERROR|FATAL" logs/app.log

# 4. Auth log failing IP breakdown (4 from 192.168.99.50, 4 from 192.168.99.51)
grep "Failed password" logs/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr

# 5. Redirection + verify + cleanup (5 lines)
grep "^.*FATAL" logs/app.log > /workspace/training_lab/tmp/fatal_only.log
wc -l /workspace/training_lab/tmp/fatal_only.log
rm -f /workspace/training_lab/tmp/fatal_only.log
