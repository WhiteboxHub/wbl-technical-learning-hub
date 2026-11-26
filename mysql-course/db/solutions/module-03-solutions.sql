-- Module 3 Reference Solutions (Instructors & Post-Attempt Verification Only)
USE training_db;

-- 1. Isolation & Pessimistic Locking
SELECT @@transaction_isolation AS current_isolation;
START TRANSACTION;
SELECT id, name, price FROM course WHERE id = 1 FOR UPDATE;
UPDATE course SET price = 525.00 WHERE id = 1;
ROLLBACK;

-- 2. Trigger verification + cleanup
INSERT INTO enrollment (student_id, course_id, enrollment_date, status, fee_paid)
VALUES (7, 1, '2025-03-01', 'active', 499.00);
SELECT * FROM enrollment_log ORDER BY id DESC LIMIT 2;
DELETE FROM enrollment WHERE student_id = 7 AND course_id = 1;
DELETE FROM enrollment_log WHERE student_id = 7 AND course_id = 1;

-- 3. Composite Index, Leftmost Prefix & SARGability
EXPLAIN ANALYZE SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-02';
CREATE INDEX idx_act_student_created ON activity_log (student_id, created_at);
EXPLAIN ANALYZE SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-02';
EXPLAIN SELECT id, student_id, created_at FROM activity_log WHERE created_at >= '2025-01-02';
EXPLAIN SELECT id FROM activity_log WHERE student_id = 3 AND YEAR(created_at) = 2025;
EXPLAIN SELECT id FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-01' AND created_at < '2026-01-01';
DROP INDEX idx_act_student_created ON activity_log;

-- 4. Pagination comparison
EXPLAIN ANALYZE SELECT id, event_type FROM activity_log ORDER BY id LIMIT 10 OFFSET 1800;
EXPLAIN ANALYZE SELECT id, event_type FROM activity_log WHERE id > 1800 ORDER BY id LIMIT 10;
