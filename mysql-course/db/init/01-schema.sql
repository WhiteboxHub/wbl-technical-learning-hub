-- Whitebox Learning: Training Management DB (MySQL 8.0)
-- Aligned with SQL & NoSQL DBMS course slides (Training Management DB)

CREATE DATABASE IF NOT EXISTS training_db;
USE training_db;

-- 1. Instructors
CREATE TABLE instructor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    specialty VARCHAR(100) NOT NULL,
    hired_date DATE NOT NULL
);

-- 2. Courses (slides 15, 16, 20, 21, 29)
CREATE TABLE course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    category VARCHAR(80) NOT NULL DEFAULT 'Engineering',
    duration_weeks INT NOT NULL DEFAULT 6 CHECK (duration_weeks > 0),
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (price >= 0),
    instructor_id INT NULL,
    CONSTRAINT fk_course_instructor
        FOREIGN KEY (instructor_id) REFERENCES instructor(id)
        ON DELETE SET NULL
);

-- 3. Subjects (slides 27, 28 - used for UNION / INTERSECT / EXCEPT demos)
CREATE TABLE subject (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE
);

-- 4. Students (slides 17, 21, 22, 25, 31, 32, 33)
CREATE TABLE student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(30) NULL,
    enrolled_date DATE NOT NULL,
    mentor_id INT NULL,
    CONSTRAINT fk_student_mentor
        FOREIGN KEY (mentor_id) REFERENCES student(id)
        ON DELETE SET NULL
);

-- 5. Enrollments (slides 21-26, 33-34)
CREATE TABLE enrollment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('active', 'completed', 'dropped') NOT NULL DEFAULT 'active',
    fee_paid DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (fee_paid >= 0),
    CONSTRAINT fk_enrollment_student
        FOREIGN KEY (student_id) REFERENCES student(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_enrollment_course
        FOREIGN KEY (course_id) REFERENCES course(id)
        ON DELETE RESTRICT,
    CONSTRAINT uq_student_course UNIQUE (student_id, course_id)
);

-- 6. Enrollment Audit Log (slide 35)
CREATE TABLE enrollment_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    action_type VARCHAR(20) NOT NULL DEFAULT 'INSERT',
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger: automatically log every new enrollment (Module 3)
DELIMITER $$
CREATE TRIGGER trg_after_enrollment_insert
AFTER INSERT ON enrollment
FOR EACH ROW
BEGIN
    INSERT INTO enrollment_log (student_id, course_id, enrollment_date, action_type)
    VALUES (NEW.student_id, NEW.course_id, NEW.enrollment_date, 'INSERT');
END$$
DELIMITER ;

-- 7. Normalization Demo Tables (slides 37-38)
CREATE TABLE users_unnormalized (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(100),      -- deliberately stores comma-separated numbers to illustrate 1NF violation
    address VARCHAR(200),
    city VARCHAR(80),
    zip_code VARCHAR(20)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE contact_info (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    phone VARCHAR(30) NOT NULL,
    address VARCHAR(200) NOT NULL,
    CONSTRAINT fk_contact_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- 8. Activity Log (2,000+ rows seeded for Module 3 EXPLAIN ANALYZE & Index tuning lab)
CREATE TABLE activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    event_type VARCHAR(40) NOT NULL,
    created_at DATETIME NOT NULL
);
