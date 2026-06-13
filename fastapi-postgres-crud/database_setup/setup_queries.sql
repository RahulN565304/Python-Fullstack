-- 1. Create the Courses Table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    duration_weeks INT NOT NULL
);

-- 2. Create the Students Table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    enrolled_course_id INT,
    FOREIGN KEY (enrolled_course_id) REFERENCES courses(course_id)
);

-- 3. Insert Clean Starter Data
INSERT INTO courses (course_name, duration_weeks) VALUES 
('Python Backend Development', 12),
('Frontend React Mastery', 8),
('Data Structures & Algorithms', 10);