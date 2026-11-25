-- Module 1 Lab: Setup Verification, Data Types, Constraints & 3NF Normalization
USE training_db;

-- 1. Verify MySQL 8.0 and inspect tables
SELECT VERSION() AS mysql_version;
SHOW TABLES;

-- 2. Create a constrained `assignment` table (PK, FK -> course(id), NOT NULL, CHECK max_score 1..100)
--    Write your CREATE TABLE statement below, test 1 valid insert, then trigger a CHECK error & FK error,
--    and DROP TABLE assignment; when done.


-- 3. Normalization (1NF -> 3NF):
--    Inspect `users_unnormalized` vs `users` + `contact_info` and write a JOIN query reconstructing clean rows.
SELECT * FROM users_unnormalized;
