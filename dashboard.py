from flask import Blueprint, render_template

from analysis import analyze
from database import get_students


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def home():
    students = [analyze(student) for student in get_students()]
    count = len(students)
    subjects = ["mathematics", "english", "science", "computer"]

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
            for key in subjects
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
        sum(student["average"] for student in students) / count
        if count else 0
    )
    highest_average = max(
        (student["average"] for student in students),
        default=0
    )
    passed = sum(1 for student in students if student["status"] != "Fail")

    return render_template(
        "index.html",
        count=count,
        class_average=round(class_average, 2),
        highest_average=highest_average,
        pass_rate=round(passed / count * 100, 2) if count else 0,
        subject_chart_data=subject_chart_data,
        gender_chart_data=gender_chart_data
    )
