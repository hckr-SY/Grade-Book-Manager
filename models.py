import uuid

class Assignment:
    def __init__(self, name, category, max_marks, assignment_id=None):
        self.id = assignment_id or str(uuid.uuid4())
        self.name = name
        self.category = category
        self.max_marks = max_marks

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "max_marks": self.max_marks
        }

    @staticmethod
    def from_dict(aid, data):
        return Assignment(
            data["name"],
            data["category"],
            data["max_marks"],
            aid
        )

class Course:
    def __init__(self, name, credit_hours):
        self.name = name
        self.credit_hours = credit_hours

        self.categories = {
            "HOMEWORK": 0.2,
            "QUIZZES": 0.2,
            "MIDTERM": 0.25,
            "FINAL_EXAM": 0.35
        }

        self.assignments = {}  # id → Assignment

    def to_dict(self):
        return {
            "credit_hours": self.credit_hours,
            "categories": self.categories,
            "assignments": {
                aid: a.to_dict() for aid, a in self.assignments.items()
            }
        }

    @staticmethod
    def from_dict(name, data):
        course = Course(name, data["credit_hours"])
        course.categories = data["categories"]

        for aid, a_data in data["assignments"].items():
            course.assignments[aid] = Assignment.from_dict(aid, a_data)

        return course

class StudentCourse:
    def __init__(self):
        self.marks = {}  # assignment_id → marks

    def to_dict(self):
        return {"marks": self.marks}

    @staticmethod
    def from_dict(data):
        sc = StudentCourse()
        sc.marks = data.get("marks", {})
        return sc

class Student:
    def __init__(self, sid, name):
        self.id = sid
        self.name = name
        self.courses = {}  # course_name → StudentCourse

    def to_dict(self):
        return {
            "name": self.name,
            "courses": {
                cname: sc.to_dict() for cname, sc in self.courses.items()
            }
        }

    @staticmethod
    def from_dict(sid, data):
        student = Student(sid, data["name"])

        for cname, sc_data in data["courses"].items():
            student.courses[cname] = StudentCourse.from_dict(sc_data)

        return student