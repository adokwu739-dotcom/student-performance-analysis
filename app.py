
from flask import Flask, render_template, request, redirect, url_for, flash
from analysis import analyze
from database import (
    init_data,
    get_students,
    get_student,
    add_student as insert_student,
    update_student as save_student,
    delete_student
)

app = Flask(__name__)
app.secret_key = "local-development-only-change-me"

init_data()


@app.route("/")
def home():
    students = [analyze(s) for s in get_students()]

    count = len(students)
    subject_chart_data = {
        "labels": [
            "Mathematics",
            "English",
            "Science",
            "Computer Studies"
        ],
        "values": [
            round(sum(student[key] for student in students) / count, 2)
            if count else 0
            for key in ["mathematics", "english", "science", "computer"]
        ]
    }
    gender_chart_data = {
        "labels": ["Female", "Male"],
        "values": [
            round(
                sum(
                    student["average"]
                    for student in students
                    if student["gender"] == gender
                )
                / sum(student["gender"] == gender for student in students),
                2
            )
            if any(student["gender"] == gender for student in students)
            else None
            for gender in ["Female", "Male"]
        ]
    }

    class_average = (
        sum(s["average"] for s in students) / count
        if count else 0
    )

    highest_average = max(
        (s["average"] for s in students),
        default=0
    )

    passed = sum(1 for s in students if s["status"] != "Fail")

    pass_rate = (passed / count * 100) if count else 0

    return render_template(
        "index.html",
        count=count,
        class_average=round(class_average, 2),
        highest_average=highest_average,
        pass_rate=round(pass_rate, 2),
        subject_chart_data=subject_chart_data,
        gender_chart_data=gender_chart_data
    )


@app.route("/students")
def student_records():
    students = [analyze(student) for student in get_students()]
    return render_template("student_records.html", students=students)


@app.route("/students/new")
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
            for subject in [
                "mathematics",
                "english",
                "science",
                "computer"
            ]
        ]
    except ValueError:
        flash("Please enter valid whole-number scores.")
        return None

    if any(score < 0 or score > 100 for score in scores):
        flash("Scores must be between 0 and 100.")
        return None

    return name, scores, gender


@app.route("/students", methods=["POST"])
def create_student():
    student_data = read_student_form()
    if student_data is None:
        return redirect(url_for("add_student"))

    name, scores, gender = student_data
    insert_student(name, *scores, gender)

    flash("Student added successfully!")
    return redirect(url_for("home"))


@app.route("/students/<int:student_id>/edit")
def edit_student(student_id):
    student = get_student(student_id)
    if student is None:
        return "Student not found", 404

    return render_template("add_student.html", student=student)


@app.route("/students/<int:student_id>/edit", methods=["POST"])
def update_student_record(student_id):
    student = get_student(student_id)
    if student is None:
        return "Student not found", 404

    student_data = read_student_form()
    if student_data is None:
        return redirect(url_for("edit_student", student_id=student_id))

    name, scores, gender = student_data
    if not save_student(student_id, name, *scores, gender):
        return "Student not found", 404

    flash("Student record updated successfully!")
    return redirect(url_for("student_records"))


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def remove_student(student_id):
    if not delete_student(student_id):
        return "Student not found", 404

    flash("Student deleted successfully.")
    return redirect(url_for("student_records"))


@app.route("/student/<int:student_id>")
def student_report(student_id):
    student = get_student(student_id)

    if student is None:
        return "Student not found", 404

    result = analyze(student)

    return render_template(
        "results.html",
        student=result
    )


if __name__ == "__main__":
    app.run(debug=True)
