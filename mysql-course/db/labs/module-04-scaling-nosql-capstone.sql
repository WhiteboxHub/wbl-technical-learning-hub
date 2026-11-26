-- Module 4 Lab: Partitioning, NoSQL Architecture & Post-Class Capstone Extension
USE training_db;

-- 1. Table Partitioning (PARTITION BY RANGE):
--    Create a temporary `_part_demo` table partitioned by created_year (p2024 < 2025, p2025 < 2026),
--    inspect INFORMATION_SCHEMA.PARTITIONS, then DROP TABLE _part_demo;

-- 2. Polyglot Persistence Decision Note (fill in below):
--    Pick the best DB (MySQL, MongoDB, Redis, Neo4j, Elasticsearch, VectorDB) for:
--    a) Student enrollments & fee payments:
--    b) Hot course cache & API rate limiting:
--    c) Typo-tolerant search across course descriptions:
--    d) Semantic Q&A over PDF lectures (RAG):

-- 3. Post-Class Capstone Extension:
--    Design 3NF `assignment` and `submission` tables (with FK, CHECK 0..100, UNIQUE(assignment_id, student_id)),
--    seed 4 assignments & 6 submissions, and write:
--    a) Average score per course for courses with >= 2 graded submissions (JOIN + GROUP BY + HAVING)
--    b) Students enrolled in course 1 who have NOT submitted Assignment 1 (LEFT JOIN anti-join)
--    c) DENSE_RANK() of submissions per assignment
