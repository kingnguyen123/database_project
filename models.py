from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    major = db.Column(db.String(100), nullable=False)

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    enroll_date = db.Column(db.Date, nullable=False)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
