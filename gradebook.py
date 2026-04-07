from models import Student, Course, Assignment, StudentCourse

class GradeBook:
    def __init__(self, students, courses):
        self.students = students
        self.courses = courses

    def add_student(self, sid, name):
        if sid not in self.students:
            self.students[sid] = Student(sid, name)

    def create_course(self, name, credits):
        if name not in self.courses:
            self.courses[name] = Course(name, credits)

    def enroll(self, sid, course_name):
        student = self.students[sid]
        if course_name not in student.courses:
            student.courses[course_name] = StudentCourse()

    def add_assignment(self, course_name, assignment):
        course = self.courses[course_name]
        course.assignments[assignment.id] = assignment

    def remove_assignment(self, course_name, assignment_id):
        if course_name not in self.courses:
            return
        
        course = self.courses[course_name]
        if assignment_id in course.assignments:
            del course.assignments[assignment_id]
        
        for student in self.students.values():
            if course_name in student.courses:
                sc = student.courses[course_name]
                if assignment_id in sc.marks:
                    del sc.marks[assignment_id]

    def get_category_average(self, sid, course_name, category):
        student = self.students[sid]
        course = self.courses[course_name]

        sc = student.courses.get(course_name)
        if not sc:
            return None

        total_earned = 0
        total_possible = 0

        for aid, assignment in course.assignments.items():
            if assignment.category == category:
                marks = sc.marks.get(aid, 0)

                total_earned += marks
                total_possible += assignment.max_marks

        if total_possible == 0:
            return None 

        return (total_earned / total_possible) * 100
    
    def get_course_grade(self, sid, course_name):
        student = self.students[sid]
        course = self.courses[course_name]

        if course_name not in student.courses:
            return 0.0, "N/A"

        total = 0
        total_weight = 0

        for category, weight in course.categories.items():
            avg = self.get_category_average(sid, course_name, category)

            if avg is not None:
                total += avg * weight
                total_weight += weight

        if total_weight == 0:
            return 0.0, "N/A"

        final_percentage = total / total_weight
        letter = self.get_letter_grade(final_percentage)

        return round(final_percentage, 2), letter
    
    def get_letter_grade(self, percentage):
        if percentage >= 90: return "A"
        elif percentage >= 80: return "B"
        elif percentage >= 70: return "C"
        elif percentage >= 60: return "D"
        else: return "F"
    
    def calculate_gpa(self, sid):
        student = self.students[sid]

        total_points = 0
        total_credits = 0

        grade_map = {
            "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0
        }

        for course_name, sc in student.courses.items():
            course = self.courses[course_name]
            percent, letter = self.get_course_grade(sid, course_name)

            if letter == "N/A":
                continue

            total_points += grade_map[letter] * course.credit_hours
            total_credits += course.credit_hours

        if total_credits == 0:
            return 0.0

        return round(total_points / total_credits, 2)
    
    def generate_transcript(self, sid):
        student = self.students[sid]
        report = []

        for course_name in student.courses:
            percent, letter = self.get_course_grade(sid, course_name)
            course = self.courses[course_name]

            report.append({
                "course": course_name,
                "credits": course.credit_hours,
                "percentage": percent,
                "grade": letter
            })

        gpa = self.calculate_gpa(sid)

        return {
            "student_id": sid,
            "name": student.name,
            "courses": report,
            "gpa": gpa
        }