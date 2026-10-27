import json
import os
import tempfile
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data.json"


def _read_students():
    with DATA_FILE.open(encoding="utf-8") as data_file:
        students = json.load(data_file)

    if not isinstance(students, list):
        raise ValueError(f"{DATA_FILE} must contain a JSON array of students.")

    return students


def _write_students(students):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            delete=False
        ) as data_file:
            temporary_path = Path(data_file.name)
            json.dump(students, data_file, indent=2, ensure_ascii=False)
            data_file.write("\n")

        os.replace(temporary_path, DATA_FILE)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def init_data():
    try:
        with DATA_FILE.open("x", encoding="utf-8") as data_file:
            json.dump([], data_file)
            data_file.write("\n")
    except FileExistsError:
        pass

    _read_students()


def get_students():
    return _read_students()


def get_student(student_id):
    return next(
        (student for student in _read_students() if student["id"] == student_id),
        None
    )


def add_student(name, mathematics, english, science, computer, gender):
    students = _read_students()
    student = {
        "id": max((record["id"] for record in students), default=0) + 1,
        "name": name,
        "mathematics": mathematics,
        "english": english,
        "science": science,
        "computer": computer,
        "gender": gender
    }
    students.append(student)
    _write_students(students)
    return student


def update_student(student_id, name, mathematics, english, science, computer, gender):
    students = _read_students()
    student = next(
        (record for record in students if record["id"] == student_id),
        None
    )
    if student is None:
        return False

    student.update({
        "name": name,
        "mathematics": mathematics,
        "english": english,
        "science": science,
        "computer": computer,
        "gender": gender
    })
    _write_students(students)
    return True


def delete_student(student_id):
    students = _read_students()
    remaining_students = [
        student for student in students if student["id"] != student_id
    ]
    if len(remaining_students) == len(students):
        return False

    _write_students(remaining_students)
    return True
