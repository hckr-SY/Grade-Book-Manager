import streamlit as st
from storage import load_data, save_data
from gradebook import GradeBook
from models import Assignment

# Load data
students, courses = load_data()
gb = GradeBook(students, courses)

st.set_page_config(page_title="GradeBook", layout="wide")
st.title("🎓 Student GradeBook System")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Add Student", "Add/Edit Course", "Enroll Student", "Enter Marks", "View Transcript"]
)

# ------------------ ADD STUDENT ------------------
if menu == "Add Student":
    st.header("👤 Manage Students")
    st.subheader("➕ Add Student")

    sid = st.text_input("Student ID")
    name = st.text_input("Name")

    if st.button("Add Student"):
        if sid and name:
            if sid in students:
                st.error("Student ID already exists!")
            else:
                gb.add_student(sid, name)
                save_data(students, courses)
                st.success("Student added!")
        else:
            st.error("Please fill all fields")

    st.divider()

    st.subheader("❌ Remove Student")
    if students:
        student_ids = list(students.keys())
        selected_sid = st.selectbox("Select Student to Remove", student_ids)

        if st.button("Remove Student"):
            if selected_sid in students:
                del students[selected_sid]
                save_data(students, courses)
                st.success(f"Student {selected_sid} removed!")
    else:
        st.info("No students available to remove")

# ------------------ ADD / EDIT COURSE ------------------
elif menu == "Add/Edit Course":
    st.header("📚 Add / Edit Course")
    categories = ["HOMEWORK", "QUIZZES", "MIDTERM", "FINAL_EXAM"]
    course_options = ["-- New Course --"] + list(courses.keys())
    
    selected_course = st.selectbox("Select Course", course_options)

    if selected_course == "-- New Course --":
        cname = st.text_input("Enter New Course Name")
    else:
        cname = selected_course

    if "course_assignments" not in st.session_state:
        st.session_state.course_assignments = {cat: [] for cat in categories}
        st.session_state.loaded_course = None

    if selected_course != st.session_state.loaded_course:
        if selected_course == "-- New Course --":
            st.session_state.course_assignments = {cat: [] for cat in categories}
        else:
            course = courses[selected_course]
            grouped = {cat: [] for cat in categories}
            for aid, a in course.assignments.items():
                grouped[a.category].append({
                    "id": aid,
                    "name": a.name,
                    "max_marks": a.max_marks
                })
            st.session_state.course_assignments = grouped
        st.session_state.loaded_course = selected_course

    course_credits = 1
    if selected_course != "-- New Course --":
        course_credits = courses[selected_course].credit_hours
    credits = st.number_input("Credit Hours", min_value=1, step=1, value=course_credits)

    st.subheader("Assignments")

    # ---------- HEADER ----------
    header_cols = st.columns(len(categories))
    for idx, category in enumerate(categories):
        with header_cols[idx]:
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"### {category}")
            with c2:
                if st.button("➕", key=f"add_{category}"):
                    st.session_state.course_assignments[category].append({
                        "id": None,
                        "name": "",
                        "max_marks": 10
                    })

    st.markdown("---")

    # ---------- GRID ----------
    max_rows = max([len(st.session_state.course_assignments[cat]) for cat in categories] + [1])

    for i in range(max_rows):
        row_cols = st.columns(len(categories), gap="medium")
        for idx, category in enumerate(categories):
            with row_cols[idx]:
                assignments = st.session_state.course_assignments[category]

                if i < len(assignments):
                    a = assignments[i]

                    c1, c2, c3 = st.columns([5, 2, 2])
                    with c1:
                        name = st.text_input("", value=a["name"], key=f"{category}_name_{i}", placeholder="Assignment", label_visibility="collapsed")
                    with c2:
                        marks = st.number_input("", min_value=1, value=a["max_marks"], key=f"{category}_marks_{i}", label_visibility="collapsed")
                    with c3:
                        st.markdown("<div style='display:flex; justify-content:center; margin-top:4px;'>", unsafe_allow_html=True)
                        remove = st.button("➖", key=f"{category}_remove_{i}")
                        st.markdown("</div>", unsafe_allow_html=True)

                    if not remove:
                        assignments[i] = {
                            "id": a.get("id"),
                            "name": name,
                            "max_marks": marks
                        }
                    else:
                        assignments.pop(i)
                        st.rerun() 
                else:
                    st.empty()

    st.divider()
    col1, col2 = st.columns([3, 1])

    # -------- SAVE COURSE --------
    with col1:
        if st.button("💾 Save Course"):
            if not cname:
                st.error("Course name required")
            else:
                if cname in courses:
                    old_ids = set(courses[cname].assignments.keys())
                else:
                    old_ids = set()
                    gb.create_course(cname, credits)

                courses[cname].credit_hours = credits
                courses[cname].assignments = {}
                new_ids = set()

                for category in categories:
                    for a in st.session_state.course_assignments[category]:
                        if a["name"]:
                            assignment = Assignment(
                                a["name"],
                                category,
                                a["max_marks"],
                                a.get("id") 
                            )
                            gb.add_assignment(cname, assignment)
                            new_ids.add(assignment.id)

                deleted_ids = old_ids - new_ids
                for student in students.values():
                    if cname in student.courses:
                        for aid in deleted_ids:
                            if aid in student.courses[cname].marks:
                                del student.courses[cname].marks[aid]

                save_data(students, courses)
                st.success("Course saved successfully!")

    # -------- DELETE COURSE --------
    with col2:
        if cname and cname in courses:
            confirm_delete = st.checkbox("Confirm delete", key="delete_course_confirm")

            if st.button("🗑️ Delete Course", key="delete_course"):
                if confirm_delete:
                    for student in students.values():
                        if cname in student.courses:
                            del student.courses[cname]

                    del courses[cname]
                    save_data(students, courses)

                    st.session_state.course_assignments = {cat: [] for cat in categories}
                    st.session_state.loaded_course = None
                    st.success(f"Course '{cname}' deleted!")
                    st.rerun()
                else:
                    st.warning("Please confirm deletion")

# ------------------ ENROLL ------------------
elif menu == "Enroll Student":
    st.header("🎯 Enroll Student")

    if not students or not courses:
        st.warning("Add students and courses first")
    else:
        sid = st.selectbox("Select Student", list(students.keys()))
        course_name = st.selectbox("Select Course", list(courses.keys()))

        if st.button("Enroll"):
            gb.enroll(sid, course_name)
            save_data(students, courses)
            st.success("Student enrolled!")

# ------------------ ENTER MARKS ------------------
elif menu == "Enter Marks":
    st.header("✍️ Enter Marks")

    if not students:
        st.warning("No students available")
    else:
        sid = st.selectbox("Select Student", list(students.keys()))
        student = students[sid]

        if not student.courses:
            st.warning("Student not enrolled in any course")
        else:
            course_name = st.selectbox("Select Course", list(student.courses.keys()))
            course = courses[course_name]
            sc = student.courses[course_name]

            categories = ["HOMEWORK", "QUIZZES", "MIDTERM", "FINAL_EXAM"]

            grouped = {cat: [] for cat in categories}
            for aid, assignment in course.assignments.items():
                grouped[assignment.category].append((aid, assignment))

            st.subheader(f"{course_name} - Marks Entry")

            for aid in course.assignments:
                key = f"{sid}_{aid}"
                if key not in st.session_state:
                    st.session_state[key] = float(sc.marks.get(aid, 0.0)) 

            # -------- HEADER --------
            header_cols = st.columns(len(categories))
            for idx, cat in enumerate(categories):
                with header_cols[idx]:
                    st.markdown(f"### {cat}")

            st.markdown("---")

            # -------- GRID --------
            max_rows = max([len(grouped[cat]) for cat in categories] + [1])
            marks_input = {}

            for i in range(max_rows):
                row_cols = st.columns(len(categories), gap="medium")
                for idx, cat in enumerate(categories):
                    with row_cols[idx]:
                        if i < len(grouped[cat]):
                            aid, assignment = grouped[cat][i]
                            c1, c2 = st.columns([3, 2])
                            with c1:
                                st.caption(assignment.name)
                            with c2:
                                marks = st.number_input(
                                    "",
                                    min_value=0.0,
                                    max_value=float(assignment.max_marks),
                                    key=f"{sid}_{aid}",
                                    label_visibility="collapsed"
                                )
                                marks_input[aid] = marks
                        else:
                            st.empty()

            st.divider()

            # -------- SAVE --------
            if st.button("Save Marks"):
                for aid, marks in marks_input.items():
                    sc.marks[aid] = marks

                save_data(students, courses)
                st.success("Marks saved successfully!")

# ------------------ TRANSCRIPT ------------------
elif menu == "View Transcript":
    st.header("📄 Transcript")

    if not students:
        st.warning("No students available")
    else:
        sid = st.selectbox("Select Student", list(students.keys()))
        transcript = gb.generate_transcript(sid)
        st.subheader(f"Student: {transcript['name']}")

        import pandas as pd

        if transcript["courses"]:
            df = pd.DataFrame(transcript["courses"])
            df = df.rename(columns={
                "course": "Course",
                "credits": "Credits",
                "percentage": "Percentage (%)",
                "grade": "Grade"
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No courses found")

        st.divider()
        st.subheader(f"🎓 GPA: {transcript['gpa']}")