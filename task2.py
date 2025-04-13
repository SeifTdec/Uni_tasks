class Person:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

class Student(Person):
    def __init__(self, name, student_id):
        super().__init__(name)
        self.__student_id = student_id
        self.__courses = []

    def enroll(self, course):
        self.__courses.append(course)

    def display_info(self):
        print(f"Name: {self.get_name()}")
        print(f"Student ID: {self.__student_id}")
        print("Registered Courses:")
        for course in self.__courses:
            print(f" - {course.get_name()}")

class Course:
    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    def get_name(self):
        return self.__name

student1 = Student("Ali", "66")
student2 = Student("Td", "77")
course1 = Course("CS101", "Introduction to Programming")
course2 = Course("CS102", "Data Structures and algorithms")

student1.enroll(course1)
student1.enroll(course2)
student2.enroll(course1)
student2.enroll(course2)


student1.display_info()
student2.display_info()
