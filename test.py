from storage import load_data, save_data
from gradebook import GradeBook
from models import Assignment

students, courses = load_data()
gb = GradeBook(students, courses)

# Add student
gb.add_student("S1", "Alice")

# Create course
gb.create_course("Math", 3)

# Enroll student
gb.enroll("S1", "Math")

# Add assignment
a1 = Assignment("HW1", "HOMEWORK", 10)
gb.add_assignment("Math", a1)

# Give marks
students["S1"].courses["Math"].marks[a1.id] = 8

# Test grade
print("Course Grade:", gb.get_course_grade("S1", "Math"))

# Save data
save_data(students, courses)