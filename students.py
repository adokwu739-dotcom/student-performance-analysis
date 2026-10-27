from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from analysis import analyze
from database import (
    add_student as insert_student,
    delete_student,
    get_student,
    get_students,
    update_student as save_student
)


students = Blueprint("students", __name__)


@students.route("/students")
def student_records():
    records = [analyze(student) for student in get_students()]
    return render_template("student_records.html", students=records)


@students.route("/students/new")
def add_student():
    return render_template("add_student.html", student=None)


def read_student_form():
    name = request.form.get("name", "").strip()
    gender = request.form.get("gender", "")

    if not name:
        flash("Student name is required.")
        return None

    if gender not in {"Female", "Male", "Not specified"}:
        flash("Please select a valid gender.")
        return None

    try:
        scores = [
            int(request.form.get(subject, ""))
            for subject in ("mathematics", "english", "science", "computer")
        ]
    except ValueError:
        flash("Please enter valid whole-number scores.")
        return None

    if any(score < 0 or score > 100 for score in scores):
        flash("Scores must be between 0 and 100.")
        return None

    return name, scores, gender


@students.route("/students", methods=["POST"])
def create_student():
    student_data = read_student_form()
    if student_data is None:
        return redirect(url_for("students.add_student"))

    name, scores, gender = student_data
    insert_student(name, *scores, gender)

    flash("Student added successfully!")
    return redirect(url_for("dashboard.home"))


@students.route("/students/<int:student_id>/edit")
def edit_student(student_id):
    student = get_student(student_id)
    if student is None:
        return "Student not found", 404

    return render_template("add_student.html", student=student)


@students.route("/students/<int:student_id>/edit", methods=["POST"])
def update_student_record(student_id):
    student = get_student(student_id)
    if student is None:
        return "Student not found", 404

    student_data = read_student_form()
    if student_data is None:
        return redirect(url_for("students.edit_student", student_id=student_id))

    name, scores, gender = student_data
    if not save_student(student_id, name, *scores, gender):
        return "Student not found", 404

    flash("Student record updated successfully!")
    return redirect(url_for("students.student_records"))


@students.route("/students/<int:student_id>/delete", methods=["POST"])
def remove_student(student_id):
    if not delete_student(student_id):
        return "Student not found", 404

    flash("Student deleted successfully.")
    return redirect(url_for("students.student_records"))


@students.route("/student/<int:student_id>")
def student_report(student_id):
    student = get_student(student_id)
    if student is None:
        return "Student not found", 404

    return render_template("results.html", student=analyze(student))
