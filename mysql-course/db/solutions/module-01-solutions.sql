-- Module 1 Reference Solutions (Instructors & Post-Attempt Verification Only)
USE training_db;

CREATE TABLE IF NOT EXISTS assignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(120) NOT NULL,
    max_score INT NOT NULL DEFAULT 100 CHECK (max_score > 0 AND max_score <= 100),
    due_date DATE NOT NULL,
    CONSTRAINT fk_assignment_course
        FOREIGN KEY (course_id) REFERENCES course(id)
        ON DELETE RESTRICT
);

INSERT INTO assignment (course_id, title, max_score, due_date)
VALUES (1, 'SQL Joins Lab', 100, '2025-03-15');

-- Expected CHECK violation (3819):
-- INSERT INTO assignment (course_id, title, max_score, due_date) VALUES (1, 'Invalid', 150, '2025-03-15');
-- Expected FK violation (1452):
-- INSERT INTO assignment (course_id, title, max_score, due_date) VALUES (999, 'Orphan', 100, '2025-03-15');

DROP TABLE IF EXISTS assignment;

-- Clean 3NF join replacing users_unnormalized
SELECT u.user_id, u.name, u.email, c.phone, c.address
FROM users u
JOIN contact_info c ON u.user_id = c.user_id
ORDER BY u.user_id, c.contact_id;
