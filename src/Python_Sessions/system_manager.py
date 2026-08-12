from typing import Dict, List
from student import Student
from course import Course


class SystemManager:
    def __init__(self) -> None:
        """
        Central manager responsible for handling students, courses,
        enrollment, and grades.
        """
        self.students: Dict[int, Student] = {}
        self.courses: Dict[int, Course] = {}

    # -------------------- Students --------------------

    def add_student(self, name: str) -> int:
        student = Student(name)
        self.students[student.student_id] = student
        return student.student_id

    def remove_student(self, student_id: int) -> None:
        if student_id not in self.students:
            raise ValueError("Student ID does not exist.")

        student = self.students[student_id]

        if student.enrolled_courses:
            raise ValueError("Cannot remove student with enrolled courses.")

        del self.students[student_id]

    def get_all_students(self) -> List[Student]:
        return list(self.students.values())

    # -------------------- Courses --------------------

    def add_course(self, name: str) -> int:
        course = Course(name)
        self.courses[course.course_id] = course
        return course.course_id

    def remove_course(self, course_id: int) -> None:
        if course_id not in self.courses:
            raise ValueError("Course ID does not exist.")

        course = self.courses[course_id]

        if course.enrolled_students:
            raise ValueError("Cannot remove course with enrolled students.")

        del self.courses[course_id]

    def get_all_courses(self) -> List[Course]:
        return list(self.courses.values())

    # -------------------- Enrollment --------------------

    def enroll_student_in_course(self, student_id: int, course_id: int) -> None:
        if student_id not in self.students:
            raise ValueError("Invalid student ID.")

        if course_id not in self.courses:
            raise ValueError("Invalid course ID.")

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id in student.enrolled_courses:
            raise ValueError("Student already enrolled in this course.")

        student.enroll_in_course(course_id)
        course.enroll_student(student_id)

    # -------------------- Grades --------------------

    def record_grade(self, student_id: int, course_id: int, grade: float) -> None:
        if student_id not in self.students:
            raise ValueError("Invalid student ID.")

        if course_id not in self.courses:
            raise ValueError("Invalid course ID.")

        student = self.students[student_id]

        if course_id not in student.enrolled_courses:
            raise ValueError("Student is not enrolled in this course.")

        student.add_grade(course_id, grade)

    # -------------------- Search --------------------

    def search_courses(self, keyword: str) -> List[Course]:
        """
        Case-insensitive partial search for courses by name.
        """
        keyword = keyword.lower()
        return [
            course
            for course in self.courses.values()
            if keyword in course.name.lower()
        ]
