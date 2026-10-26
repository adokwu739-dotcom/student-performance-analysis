
import sqlite3

DATABASE = "students.db"

STUDENTS = [
    ("Maria Adams", 88, 76, 91, 72),
    ("Joshua Israel", 94, 89, 97, 91),
    ("Williams Atubu", 67, 72, 58, 64),
    ("Samuel Adamu", 45, 58, 52, 61),
    ("Inyang Emmanuel", 79, 84, 73, 88),
    ("Fatima Ezekiel", 91, 95, 88, 86),
    ("George Raphael", 55, 48, 62, 51),
    ("Samuel Akoji", 82, 91, 79, 84)
]


def connect():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mathematics INTEGER NOT NULL,
                english INTEGER NOT NULL,
                science INTEGER NOT NULL,
                computer INTEGER NOT NULL
            )
        """)

        count = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        if count == 0:
            connection.executemany("""
                INSERT INTO students
                (name, mathematics, english, science, computer)
                VALUES (?, ?, ?, ?, ?)
            """, STUDENTS)


def get_students():
    with connect() as connection:
        rows = connection.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]


def get_student(student_id):
    with connect() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

        return dict(row) if row else None


def add_student(name, mathematics, english, science, computer):
    with connect() as connection:
        connection.execute("""
            INSERT INTO students
            (name, mathematics, english, science, computer)
            VALUES (?, ?, ?, ?, ?)
        """, (name, mathematics, english, science, computer))


def delete_student(student_id):
    with connect() as connection:
        connection.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
