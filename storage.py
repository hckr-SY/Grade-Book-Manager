import json
import os
from models import Student, Course

DB_PATH = "data/db.json"

def load_data():
    if not os.path.exists(DB_PATH):
        return {}, {}

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    students = {}
    courses = {}

    for sid, s_data in data.get("students", {}).items():
        students[sid] = Student.from_dict(sid, s_data)

    for cname, c_data in data.get("courses", {}).items():
        courses[cname] = Course.from_dict(cname, c_data)

    return students, courses

def save_data(students, courses):
    data = {
        "students": {
            sid: s.to_dict() for sid, s in students.items()
        },
        "courses": {
            cname: c.to_dict() for cname, c in courses.items()
        }
    }

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)