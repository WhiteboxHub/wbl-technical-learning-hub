-- Seed data for Whitebox Learning Training Management DB
USE training_db;

INSERT INTO instructor (id, name, email, specialty, hired_date) VALUES
(1, 'Dr. Maya Lin', 'maya.lin@wbl.edu', 'Data Science & ML', '2021-02-15'),
(2, 'Carlos Rivera', 'carlos.rivera@wbl.edu', 'Backend & Databases', '2020-08-01'),
(3, 'Priya Nair', 'priya.nair@wbl.edu', 'Cloud & Security', '2022-04-10');

-- Courses (matches slide 29 + additional realistic courses; course 6 has 0 enrollments for RIGHT/FULL JOIN demos)
INSERT INTO course (id, name, description, category, duration_weeks, price, instructor_id) VALUES
(1, 'Data Science', 'Introduction to Data Science concepts', 'Data', 8, 499.00, 1),
(2, 'Web Development', 'Learn frontend and backend development', 'Engineering', 10, 399.00, 2),
(3, 'Machine Learning', 'Deep dive into ML algorithms', 'AI', 8, 599.00, 1),
(4, 'Cybersecurity', 'Protecting digital assets from attacks', 'Security', 6, 449.00, 3),
(5, 'Cloud Computing', 'Managing infrastructure on the cloud', 'Cloud', 6, 499.00, 3),
(6, 'Quantum Computing', 'Foundations of quantum algorithms (upcoming)', 'Research', 4, 699.00, NULL);

-- Subjects (includes overlap with course.name for UNION / INTERSECT / EXCEPT demos)
INSERT INTO subject (id, name, code) VALUES
(1, 'SQL Fundamentals', 'DB101'),
(2, 'Data Science', 'DS101'),
(3, 'Cloud Computing', 'CL101'),
(4, 'Python Programming', 'PY101'),
(5, 'Distributed Systems', 'CS301');

-- Students (Alice matches slide 21; includes students with NULL phone, NULL mentor_id, and 0 enrollments)
INSERT INTO student (id, first_name, last_name, email, phone, enrolled_date, mentor_id) VALUES
(1, 'Alice', 'Johnson', 'alice.johnson@example.com', '555-0101', '2025-01-10', NULL),
(2, 'Bob', 'Smith', 'bob.smith@example.com', '555-0102', '2025-01-12', 1),
(3, 'Charlie', 'Brown', 'charlie.brown@example.com', NULL, '2025-01-15', 1),
(4, 'Diana', 'Prince', 'diana.prince@example.com', '555-0104', '2025-01-20', 2),
(5, 'Evan', 'Wright', 'evan.wright@example.com', '555-0105', '2025-02-01', 2),
(6, 'Fatima', 'Al-Zahra', 'fatima.zahra@example.com', NULL, '2025-02-05', NULL),
(7, 'George', 'Miller', 'george.miller@example.com', '555-0107', '2025-02-10', 4),
(8, 'Hannah', 'Abbott', 'hannah.abbott@example.com', '555-0108', '2025-02-14', 1);
-- Note: Students 7 (George) and 8 (Hannah) have NO enrollments (for LEFT JOIN & IS NULL demos).

-- Enrollments (triggers trg_after_enrollment_insert automatically!)
INSERT INTO enrollment (student_id, course_id, enrollment_date, status, fee_paid) VALUES
(1, 1, '2025-01-11', 'completed', 499.00),
(1, 2, '2025-01-15', 'active', 399.00),
(1, 3, '2025-02-01', 'active', 599.00),
(2, 1, '2025-01-13', 'active', 499.00),
(2, 4, '2025-01-25', 'dropped', 0.00),
(3, 1, '2025-01-16', 'completed', 499.00),
(3, 5, '2025-02-02', 'active', 499.00),
(4, 2, '2025-01-21', 'completed', 399.00),
(4, 3, '2025-02-03', 'active', 599.00),
(5, 2, '2025-02-02', 'active', 399.00),
(5, 5, '2025-02-10', 'active', 499.00),
(6, 4, '2025-02-06', 'active', 449.00);

-- Normalization demo rows (slides 37-38)
INSERT INTO users_unnormalized VALUES
(1, 'Alice Johnson', 'alice@example.com', '555-0101, 555-0199', '100 Main St, Austin, TX', 'Austin', '78701'),
(2, 'Bob Smith', 'bob@example.com', '555-0102', '200 Oak Ave, San Jose, CA', 'San Jose', '95112');

INSERT INTO users VALUES
(1, 'Alice Johnson', 'alice@example.com'),
(2, 'Bob Smith', 'bob@example.com');

INSERT INTO contact_info (user_id, phone, address) VALUES
(1, '555-0101', '100 Main St, Austin, TX 78701'),
(1, '555-0199', '100 Main St, Austin, TX 78701'),
(2, '555-0102', '200 Oak Ave, San Jose, CA 95112');

-- Seed 2,000 activity_log rows using MySQL 8.0 recursive CTE (for Module 3 EXPLAIN ANALYZE & indexing demo)
SET SESSION cte_max_recursion_depth = 2500;
INSERT INTO activity_log (student_id, course_id, event_type, created_at)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 2000
)
SELECT
    1 + (n % 8),
    1 + (n % 5),
    CASE n % 4
        WHEN 0 THEN 'login'
        WHEN 1 THEN 'video_play'
        WHEN 2 THEN 'quiz_submit'
        ELSE 'lab_complete'
    END,
    DATE_ADD('2025-01-01 08:00:00', INTERVAL n MINUTE)
FROM seq;
