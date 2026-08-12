class Student:
    _id_counter = 1

    def __init__(self, name: str):
        self.student_id = Student._id_counter
        Student._id_counter += 1

        self.name = name
        self.enrolled_courses: list[int] = []
        self.grades: dict[int, float] = {}

    def enroll_in_course(self, course_id: int) -> None:
        if course_id in self.enrolled_courses:
            raise EnrollmentError("Already enrolled in this course.")
        self.enrolled_courses.append(course_id)

    def add_grade(self, course_id: int, grade: float) -> None:
        if course_id not in self.enrolled_courses:
            raise EnrollmentError("Student not enrolled in this course.")
        self.grades[course_id] = grade
