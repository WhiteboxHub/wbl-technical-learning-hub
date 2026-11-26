#!/usr/bin/env bash
# Capstone fault injector (Module 4). Usage: scripts/break.sh <fault>   Undo: scripts/fix.sh
# Faults: duplicate-join | missing-index | broken-trigger | null-trap | orphan-fk | stale-cache
# The instructor runs this; candidates diagnose from SQL evidence (row counts, EXPLAIN, SHOW TRIGGERS, logs) before fixing.
set -e
cd "$(dirname "$0")/.."

run_sql() {
  docker compose exec -T mysql mysql -uroot -proot -D training_db -e "$1"
}

case "${1:-}" in
  duplicate-join)
    # Creates a reporting view with a broken many-to-many join (missing join condition / wrong key) that inflates totals
    run_sql "CREATE OR REPLACE VIEW v_course_revenue_report AS
      SELECT c.id, c.name, COUNT(e.id) AS enrollment_count, SUM(e.fee_paid) AS total_revenue
      FROM course c
      JOIN enrollment e ON c.category <> ''
      GROUP BY c.id, c.name;"
    echo "fault injected: duplicate-join (query SELECT * FROM v_course_revenue_report;)"
    ;;
  missing-index)
    # Drops any secondary index on activity_log(student_id) so lookups fall back to a full table scan (type: ALL)
    run_sql "DROP INDEX idx_act_student_created ON activity_log;" >/dev/null 2>&1 || true
    run_sql "DROP INDEX idx_activity_student ON activity_log;" >/dev/null 2>&1 || true
    echo "fault injected: missing-index (run EXPLAIN ANALYZE SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3;)"
    ;;
  broken-trigger)
    # Drops the audit trigger so new enrollments silently stop logging to enrollment_log
    run_sql "DROP TRIGGER IF EXISTS trg_after_enrollment_insert;"
    echo "fault injected: broken-trigger (insert into enrollment and check enrollment_log)"
    ;;
  null-trap)
    # Creates a broken view using NOT IN with a subquery that contains NULL (returns 0 rows)
    run_sql "CREATE OR REPLACE VIEW v_unassigned_mentors AS
      SELECT id, first_name, last_name FROM student
      WHERE id NOT IN (SELECT mentor_id FROM student);"
    echo "fault injected: null-trap (query SELECT * FROM v_unassigned_mentors;)"
    ;;
  orphan-fk)
    # Temporarily inserts an invalid course_id row with FK checks bypassed to simulate dirty legacy import
    run_sql "SET FOREIGN_KEY_CHECKS=0;
      INSERT INTO enrollment (id, student_id, course_id, enrollment_date, status, fee_paid)
      VALUES (999, 1, 9999, '2025-03-01', 'active', 100.00)
      ON DUPLICATE KEY UPDATE course_id = 9999;
      SET FOREIGN_KEY_CHECKS=1;"
    echo "fault injected: orphan-fk (enrollment id=999 points to non-existent course_id=9999)"
    ;;
  stale-cache)
    # Writes stale course list into Redis with a 1-hour TTL that disagrees with MySQL
    docker compose exec -T redis redis-cli SET "courses:active" '[{"id":1,"name":"Data Science","price":9999.00},{"id":2,"name":"Legacy Course","price":10.00}]' EX 3600 >/dev/null
    echo "fault injected: stale-cache (Redis key courses:active has stale data while MySQL has 6 courses)"
    ;;
  *)
    echo "usage: scripts/break.sh duplicate-join|missing-index|broken-trigger|null-trap|orphan-fk|stale-cache"
    exit 1
    ;;
esac
