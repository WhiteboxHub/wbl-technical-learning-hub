-- Module 4 Reference Solutions (Instructors & Post-Attempt Verification Only)
USE training_db;

-- 1. Partitioning demo
CREATE TABLE _part_demo (
    id INT NOT NULL,
    created_year INT NOT NULL,
    PRIMARY KEY (id, created_year)
) PARTITION BY RANGE (created_year) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);
SELECT PARTITION_NAME, TABLE_ROWS
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_SCHEMA = 'training_db' AND TABLE_NAME = '_part_demo';
DROP TABLE _part_demo;

-- 2. Polyglot answers:
-- a) Enrollments & payments -> MySQL (ACID + FK constraints)
-- b) Hot cache & rate limiting -> Redis (sub-ms RAM + TTL + atomic INCR)
-- c) Typo-tolerant course search -> Elasticsearch (Lucene inverted index)
-- d) Semantic Q&A over PDFs -> VectorDB (embeddings + cosine similarity)

-- 3. Post-Class Capstone Solution
CREATE TABLE IF NOT EXISTS assignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(120) NOT NULL,
    max_score INT NOT NULL DEFAULT 100 CHECK (max_score > 0 AND max_score <= 100),
    due_date DATE NOT NULL,
    CONSTRAINT fk_cap_assignment_course
        FOREIGN KEY (course_id) REFERENCES course(id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS submission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    student_id INT NOT NULL,
    submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5, 2) NULL CHECK (score >= 0 AND score <= 100),
    CONSTRAINT fk_cap_sub_assignment
        FOREIGN KEY (assignment_id) REFERENCES assignment(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cap_sub_student
        FOREIGN KEY (student_id) REFERENCES student(id)
        ON DELETE RESTRICT,
    CONSTRAINT uq_assignment_student UNIQUE (assignment_id, student_id)
);

INSERT INTO assignment (id, course_id, title, max_score, due_date) VALUES
(1, 1, 'Pandas Cleaning Lab', 100, '2025-02-01'),
(2, 1, 'EDA Storytelling Deck', 100, '2025-02-15'),
(3, 2, 'REST API Design', 100, '2025-02-10'),
(4, 3, 'Logistic Regression Baseline', 100, '2025-02-20')
ON DUPLICATE KEY UPDATE title = VALUES(title);

INSERT INTO submission (assignment_id, student_id, score) VALUES
(1, 1, 95.00),
(1, 2, 88.00),
(2, 1, 92.00),
(3, 1, 90.00),
(3, 4, 84.00),
(3, 5, 79.00)
ON DUPLICATE KEY UPDATE score = VALUES(score);

-- a) Average score per course (>= 2 graded submissions)
SELECT c.name AS course_name, COUNT(sub.id) AS graded_submissions, ROUND(AVG(sub.score), 2) AS avg_score
FROM course c
JOIN assignment a ON a.course_id = c.id
JOIN submission sub ON sub.assignment_id = a.id
WHERE sub.score IS NOT NULL
GROUP BY c.id, c.name
HAVING COUNT(sub.id) >= 2;

-- b) Students enrolled in course 1 who have NOT submitted Assignment 1 (Expected: Charlie Brown)
SELECT s.id, s.first_name, s.last_name
FROM student s
JOIN enrollment e ON e.student_id = s.id AND e.course_id = 1
LEFT JOIN submission sub ON sub.student_id = s.id AND sub.assignment_id = 1
WHERE sub.id IS NULL;

-- c) DENSE_RANK per assignment
SELECT a.title, s.first_name, sub.score,
       DENSE_RANK() OVER (PARTITION BY sub.assignment_id ORDER BY sub.score DESC) AS rank_in_assignment
FROM submission sub
JOIN assignment a ON sub.assignment_id = a.id
JOIN student s ON sub.student_id = s.id
ORDER BY sub.assignment_id, rank_in_assignment;
