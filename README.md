
---

# 📌 Project 2: Student GradeBook System

```markdown
# 🎓 Student GradeBook System

A flexible gradebook system designed to manage student performance across courses using weighted grading and GPA calculation.

## 🚀 Features

- Supports multiple students and courses
- Weighted grading system:

  | Category     | Weight |
  |-------------|--------|
  | Homework    | 20%    |
  | Quizzes     | 20%    |
  | Midterm     | 25%    |
  | Final Exam  | 35%    |

- Assignment tracking per category
- Automatic grade calculation:
  - Category averages
  - Final course percentage
  - Letter grades
  - GPA calculation

- GPA Scale:
  - A → 4.0
  - B → 3.0
  - C → 2.0
  - D → 1.0
  - F → 0.0

- Transcript generation:
  - Course-wise performance
  - Final grades
  - Cumulative GPA

---

## 🏗️ System Design

### Classes

- **Assignment**
  - name
  - pointsEarned
  - pointsPossible
  - category

- **Course**
  - courseName
  - creditHours
  - categories (weights)
  - assignments

- **Student**
  - studentId
  - name
  - courses

- **GradeBook**
  - students (map)
  - Core system logic

---

## ⚙️ Key Logic

- Category score = average of assignments
- Final grade = weighted sum of categories
- GPA = weighted by credit hours

### Edge Case Handling

- Missing assignments → treated as 0
- Empty categories → excluded from calculation

---

## 🧪 Demonstration

Includes:
- Multiple students
- 2–3 courses per student
- Different assignment distributions
- Realistic grade computation

---

## ▶️ How to Run

### Python
```bash
streamlit run app.py