class Student:

    _id_counter = 1  # Class Attribute

    def __init__(self, name):
        self.student_id = Student._id_counter
        Student._id_counter += 1

        self.name = name
        self.grades = {}
        self.enrolled_course = []

    def __str__(self):
        return (
            f"Student ID : {self.student_id}\n"
            f"Name       : {self.name}\n"
            f"Grades     : {self.grades}\n"
            f"Courses    : {self.enrolled_course}"
        )

    def __repr__(self):
        return (
            f"Student("
            f"id={self.student_id}, "
            f"name='{self.name}', "
            f"grades={self.grades}, "
            f"courses={self.enrolled_course}"
            f")"
        )

    def add_grade(self, course_id, grade):
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")

        self.grades[course_id] = grade

    def enroll_in_course(self, course):
        if course in self.enrolled_course:
            raise ValueError("Student is already enrolled in this course")

        self.enrolled_course.append(course)


