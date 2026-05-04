# Normalization Report

## Original Functional Dependencies
The original unnormalized idea for the project can be written like this:

`Registration(student_name, student_email, major, course_name, instructor, max_capacity, enroll_date)`

The main functional dependencies are:
- `student_email -> student_name, major`
- `course_name -> instructor, max_capacity`
- `(student_email, course_name) -> enroll_date`

## Anomaly Identification
### Update anomaly
If a student's name, email, or major changes, that same information may need to be updated in many rows. The same problem happens if course information changes.

### Insertion anomaly
It would be hard to add a new student or a new course if there is no enrollment yet, because everything is stored in one large table.

### Deletion anomaly
If the last enrollment row for a student or course is deleted, important student or course information could also be lost.

## Decomposition Steps
To remove redundancy and reduce anomalies, the original table is decomposed into three smaller tables:

1. `students(student_id, name, email, major)`
2. `courses(course_id, course_name, instructor, max_capacity)`
3. `enrollments(enrollment_id, student_id, course_id, enroll_date)`

This decomposition separates student data, course data, and relationship data into their own tables.

## Final Relational Schema
The Python application will use the following schema:

- `students`
  - `student_id` primary key
  - `name`
  - `email` unique
  - `major`
- `courses`
  - `course_id` primary key
  - `course_name`
  - `instructor`
  - `max_capacity`
- `enrollments`
  - `enrollment_id` primary key
  - `student_id` foreign key
  - `course_id` foreign key
  - `enroll_date`
  - unique combination of `student_id` and `course_id`

The final structure is in 3rd Normal Form because student facts depend only on the student key, course facts depend only on the course key, and enrollment facts depend only on the enrollment record.
