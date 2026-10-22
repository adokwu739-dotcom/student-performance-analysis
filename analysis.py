
SUBJECTS = ["Mathematics", "English", "Science", "Computer Studies"]

def grade_for(average):
    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"

def analyze(student):
    scores = [
        student["mathematics"],
        student["english"],
        student["science"],
        student["computer"]
    ]

    total = sum(scores)
    average = total / len(scores)

    highest = max(scores)
    lowest = min(scores)

    return {
        **student,
        "total": total,
        "average": round(average, 2),
        "grade": grade_for(average),
        "status": "Pass" if average >= 50 else "Fail",
        "best_subject": SUBJECTS[scores.index(highest)],
        "weakest_subject": SUBJECTS[scores.index(lowest)]
    }