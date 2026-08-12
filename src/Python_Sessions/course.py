class Course:
    _id_counter = 1

    def __init__(self, name: str):
        self.course_id = Course._id_counter
        Course._id_counter += 1

        self.name = name
        self.enrolled_students: list[int] = []

    def enroll_student(self, student_id: int) -> None:
        if student_id in self.enrolled_students:
            raise EnrollmentError("Student already enrolled.")
        self.enrolled_students.append(student_id)
