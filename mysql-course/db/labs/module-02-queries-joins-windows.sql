-- Module 2 Lab: CRUD, NULLs, GROUP BY/HAVING, Joins, CTEs & Window Functions
USE training_db;

-- Predict the expected row count BEFORE running each query!

-- 1. NULL check + Aggregates:
--    Find students without a phone number (IS NULL), then show course_id, count, and revenue
--    for non-dropped enrollments where count > 1 (WHERE + GROUP BY + HAVING).

-- 2. LEFT JOIN Anti-Join:
--    Find all students who have ZERO enrollments (expected: 2 rows).

-- 3. NOT EXISTS vs NOT IN NULL trap:
--    Find all students who are NOT mentors to anyone using NOT EXISTS (expected: 5 rows).

-- 4. Recursive CTE:
--    Use WITH RECURSIVE on student(id, first_name, mentor_id) to display depth (0 for top mentors) and mentor chain.

-- 5. Window Functions:
--    a) Using a CTE + ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY fee_paid DESC, enrollment_date ASC),
--       return each enrolled student's single highest-fee course (expected: 6 rows).
--    b) Show each non-dropped enrollment ordered by enrollment_date, id with a running SUM(fee_paid) total.
