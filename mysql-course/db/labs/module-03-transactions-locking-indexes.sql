-- Module 3 Lab: Transactions, Locking, Triggers, Composite Indexing & EXPLAIN ANALYZE
USE training_db;

-- 1. Transaction & Locking:
--    Check @@transaction_isolation, then run START TRANSACTION; SELECT ... FOR UPDATE on course id = 1;
--    update price temporarily, verify inside tx, then ROLLBACK.

-- 2. Audit Trigger:
--    Insert an enrollment for student 7 in course 1, verify enrollment_log recorded it automatically,
--    then clean up both test rows.

-- 3. Composite Index, Leftmost Prefix & SARGability:
--    a) Run EXPLAIN ANALYZE on: SELECT id, student_id, created_at FROM activity_log WHERE student_id = 3 AND created_at >= '2025-01-02';
--    b) CREATE INDEX idx_act_student_created ON activity_log (student_id, created_at); and re-run EXPLAIN ANALYZE.
--    c) Observe what happens when you omit student_id OR wrap created_at in YEAR(created_at) = 2025.
--    d) Drop idx_act_student_created afterwards.

-- 4. Pagination (OFFSET vs Keyset):
--    Compare EXPLAIN ANALYZE for LIMIT 10 OFFSET 1800 vs WHERE id > 1800 ORDER BY id LIMIT 10.
EXPLAIN ANALYZE SELECT id, event_type FROM activity_log ORDER BY id LIMIT 10 OFFSET 1800;
