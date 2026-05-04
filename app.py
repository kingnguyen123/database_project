from flask import Flask, flash, redirect, render_template, request, url_for

from models import Course, Student, db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)


def validate_student_form(form_data, current_student_id=None):
    name = form_data.get("name", "").strip()
    email = form_data.get("email", "").strip()
    major = form_data.get("major", "").strip()
    errors = []

    if not name:
        errors.append("Student name is required.")
    if not email:
        errors.append("Student email is required.")
    elif "@" not in email or "." not in email:
        errors.append("Student email must be a valid email address.")
    if not major:
        errors.append("Student major is required.")

    existing_student = Student.query.filter_by(email=email).first()
    if existing_student and existing_student.student_id != current_student_id:
        errors.append("That email address is already being used by another student.")

    cleaned_data = {
        "name": name,
        "email": email,
        "major": major,
    }
    return cleaned_data, errors


def validate_course_form(form_data):
    course_name = form_data.get("course_name", "").strip()
    instructor = form_data.get("instructor", "").strip()
    max_capacity_raw = form_data.get("max_capacity", "").strip()
    errors = []
    max_capacity = None

    if not course_name:
        errors.append("Course name is required.")
    if not instructor:
        errors.append("Instructor name is required.")
    if not max_capacity_raw:
        errors.append("Maximum capacity is required.")
    else:
        try:
            max_capacity = int(max_capacity_raw)
            if max_capacity <= 0:
                errors.append("Maximum capacity must be greater than 0.")
        except ValueError:
            errors.append("Maximum capacity must be a whole number.")

    cleaned_data = {
        "course_name": course_name,
        "instructor": instructor,
        "max_capacity": max_capacity_raw,
    }
    return cleaned_data, max_capacity, errors


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students")
def students():
    student_list = Student.query.order_by(Student.student_id.asc()).all()
    return render_template("students.html", students=student_list)


@app.route("/students/new", methods=["GET", "POST"])
def new_student():
    form_data = {"name": "", "email": "", "major": ""}

    if request.method == "POST":
        form_data, errors = validate_student_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "student_form.html",
                form_data=form_data,
                form_title="Add Student",
                submit_label="Create Student",
            )

        student = Student(
            name=form_data["name"],
            email=form_data["email"],
            major=form_data["major"],
        )
        db.session.add(student)
        db.session.commit()
        flash("Student created successfully.", "success")
        return redirect(url_for("students"))

    return render_template(
        "student_form.html",
        form_data=form_data,
        form_title="Add Student",
        submit_label="Create Student",
    )


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        form_data, errors = validate_student_form(request.form, current_student_id=student.student_id)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "student_form.html",
                form_data=form_data,
                form_title="Edit Student",
                submit_label="Save Changes",
            )

        student.name = form_data["name"]
        student.email = form_data["email"]
        student.major = form_data["major"]
        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("students"))

    form_data = {
        "name": student.name,
        "email": student.email,
        "major": student.major,
    }
    return render_template(
        "student_form.html",
        form_data=form_data,
        form_title="Edit Student",
        submit_label="Save Changes",
    )


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students"))


@app.route("/courses")
def courses():
    course_list = Course.query.order_by(Course.course_id.asc()).all()
    return render_template("courses.html", courses=course_list)


@app.route("/courses/new", methods=["GET", "POST"])
def new_course():
    form_data = {"course_name": "", "instructor": "", "max_capacity": ""}

    if request.method == "POST":
        form_data, max_capacity, errors = validate_course_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "course_form.html",
                form_data=form_data,
                form_title="Add Course",
                submit_label="Create Course",
            )

        course = Course(
            course_name=form_data["course_name"],
            instructor=form_data["instructor"],
            max_capacity=max_capacity,
        )
        db.session.add(course)
        db.session.commit()
        flash("Course created successfully.", "success")
        return redirect(url_for("courses"))

    return render_template(
        "course_form.html",
        form_data=form_data,
        form_title="Add Course",
        submit_label="Create Course",
    )


@app.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == "POST":
        form_data, max_capacity, errors = validate_course_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "course_form.html",
                form_data=form_data,
                form_title="Edit Course",
                submit_label="Save Changes",
            )

        course.course_name = form_data["course_name"]
        course.instructor = form_data["instructor"]
        course.max_capacity = max_capacity
        db.session.commit()
        flash("Course updated successfully.", "success")
        return redirect(url_for("courses"))

    form_data = {
        "course_name": course.course_name,
        "instructor": course.instructor,
        "max_capacity": str(course.max_capacity),
    }
    return render_template(
        "course_form.html",
        form_data=form_data,
        form_title="Edit Course",
        submit_label="Save Changes",
    )


@app.route("/courses/<int:course_id>/delete", methods=["POST"])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted successfully.", "success")
    return redirect(url_for("courses"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
