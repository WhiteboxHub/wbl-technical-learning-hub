#!/usr/bin/env bash
# Undo every injected capstone fault and restore the healthy Training Management DB baseline.
set -e
cd "$(dirname "$0")/.."

docker compose exec -T mysql mysql -uroot -proot -D training_db <<'SQL'
DROP VIEW IF EXISTS v_course_revenue_report;
DROP VIEW IF EXISTS v_unassigned_mentors;
DROP TABLE IF EXISTS _part_demo;
DROP FUNCTION IF EXISTS fn_discounted_price;
DELETE FROM enrollment WHERE id = 999;

DROP TRIGGER IF EXISTS trg_after_enrollment_insert;
DELIMITER $$
CREATE TRIGGER trg_after_enrollment_insert
AFTER INSERT ON enrollment
FOR EACH ROW
BEGIN
    INSERT INTO enrollment_log (student_id, course_id, enrollment_date, action_type)
    VALUES (NEW.student_id, NEW.course_id, NEW.enrollment_date, 'INSERT');
END$$
DELIMITER ;
SQL

docker compose exec -T redis redis-cli DEL "courses:active" >/dev/null 2>&1 || true

echo "all faults cleared (views dropped, orphan row removed, trigger restored, Redis cache cleared)"
