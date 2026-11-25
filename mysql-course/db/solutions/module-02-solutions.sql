-- Module 2 Reference Solutions (Instructors & Post-Attempt Verification Only)
USE training_db;

-- 1. NULL check + Aggregates (Expected: 2 NULL phones; 4 courses with >1 non-dropped enrollment)
SELECT id, first_name, last_name FROM student WHERE phone IS NULL;

SELECT course_id, COUNT(*) AS enrollments, SUM(fee_paid) AS revenue
FROM enrollment
WHERE status <> 'dropped'
GROUP BY course_id
HAVING COUNT(*) > 1
ORDER BY enrollments DESC;

-- 2. LEFT JOIN anti-join (Expected: 2 students: George Miller, Hannah Abbott)
SELECT s.id, s.first_name, s.last_name
FROM student s
LEFT JOIN enrollment e ON s.id = e.student_id
WHERE e.id IS NULL;

-- 3. NOT EXISTS (Expected: 5 non-mentors: 3, 5, 6, 7, 8)
SELECT s.id, s.first_name, s.last_name
FROM student s
WHERE NOT EXISTS (SELECT 1 FROM student m WHERE m.mentor_id = s.id)
ORDER BY s.id;

-- 4. Recursive CTE mentor chain (Expected: 8 rows, max depth 3)
WITH RECURSIVE mentor_tree AS (
    SELECT id, first_name, mentor_id, 0 AS depth, CAST(first_name AS CHAR(200)) AS chain
    FROM student
    WHERE mentor_id IS NULL
    UNION ALL
    SELECT s.id, s.first_name, s.mentor_id, mt.depth + 1, CONCAT(mt.chain, ' -> ', s.first_name)
    FROM student s
    JOIN mentor_tree mt ON s.mentor_id = mt.id
)
SELECT id, first_name, depth, chain
FROM mentor_tree
ORDER BY depth, id;

-- 5a. Window Function: Top-1 highest-fee course per student (Expected: 6 rows)
WITH ranked_enrollments AS (
    SELECT
        s.id AS student_id,
        s.first_name,
        c.name AS course_name,
        e.fee_paid,
        ROW_NUMBER() OVER (
            PARTITION BY e.student_id
            ORDER BY e.fee_paid DESC, e.enrollment_date ASC
        ) AS rn
    FROM enrollment e
    JOIN student s ON e.student_id = s.id
    JOIN course c ON e.course_id = c.id
)
SELECT student_id, first_name, course_name, fee_paid
FROM ranked_enrollments
WHERE rn = 1
ORDER BY student_id;

-- 5b. Running revenue total + LAG (Expected: 11 rows)
SELECT
    id,
    enrollment_date,
    student_id,
    fee_paid,
    SUM(fee_paid) OVER (ORDER BY enrollment_date, id) AS running_revenue,
    LAG(fee_paid) OVER (ORDER BY enrollment_date, id) AS prev_fee
FROM enrollment
WHERE status <> 'dropped'
ORDER BY enrollment_date, id;
