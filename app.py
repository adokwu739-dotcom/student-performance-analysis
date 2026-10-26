
from flask import Flask, render_template, request, redirect, url_for, flash
from analysis import analyze
from database import (
    init_db,
    get_students,
    get_student,
    add_student,
    delete_student
)

app = Flask(__name__)
app.secret_key = "local-development-only-change-me"

init_db()


@app.route("/")
def home():
    students = [analyze(s) for s in get_students()]

    count = len(students)

    class_average = (
        sum(s["average"] for s in students) / count
        if count else 0
    )

    highest_average = max(
        (s["average"] for s in students),
        default=0
    )

    passed = sum(
        1 for s in students if s["status"] == "Pass"
    )

    pass_rate = (passed / count * 100) if count else 0

    return render_template(
        "index.html",
        students=students,
        count=count,
        class_average=round(class_average, 2),
        highest_average=highest_average,
        pass_rate=round(pass_rate, 2)
    )


@app.route("/students", methods=["POST"])
def create_student():
    name = request.form.get("name", "").strip()

    if not name:
        flash("Student name is required.")
        return redirect(url_for("home"))

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
        return redirect(url_for("home"))

    if any(score < 0 or score > 100 for score in scores):
        flash("Scores must be between 0 and 100.")
        return redirect(url_for("home"))

    add_student(name, *scores)

    flash("Student added successfully!")
    return redirect(url_for("home"))


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


@app.route("/student/<int:student_id>/delete", methods=["POST"])
def remove_student(student_id):
    delete_student(student_id)
    flash("Student deleted successfully.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
