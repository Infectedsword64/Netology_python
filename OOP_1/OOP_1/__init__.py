class Student:
    def __init__(self, name, lastname, gender):
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.lastname}\n"
                f"Средняя оценка за домашние задания: {self.__average_grade()}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершённые курсы: {', '.join(self.finished_courses)}")

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lec, course, grade):
        if isinstance(lec, Lecturer) and course in lec.courses_attached and course in self.courses_in_progress:
            if course in lec.grades:
                lec.grades[course] += [grade]
            else:
                lec.grades[course] = [grade]
        else:
            return "Ошибка"

    def __average_grade(self):
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return total / count if count != 0 else 0


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {self.__average_grade()}")

    def __average_grade(self):
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return total / count if count != 0 else 0


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return "Ошибка"

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Функция для подсчёта средней оценки за ДЗ по всем студентам на курсе
def average_hw_grade(students, course_name):
    all_grades = []
    for student in students:
        if course_name in student.grades:
            all_grades.extend(student.grades[course_name])
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


def average_lecture_grade(lecturers, course_name):
    all_grades = []
    for lecturer in lecturers:
        if course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


student1 = Student('Ольга', 'Алёхина', 'Ж')
student2 = Student('Алексей', 'Ольгин', 'М')

lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Роман', 'Романов')

reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Олег', 'Сас')

student1.courses_in_progress += ['Python', 'Java']
student2.courses_in_progress += ['Python', 'C++']

lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'Java']

reviewer1.courses_attached += ['Python', 'Java']
reviewer2.courses_attached += ['Python', 'C++']

# 1. Студенты оценивают лекторов
print(student1.rate_lecture(lecturer1, 'Python', 9))   # None
print(student1.rate_lecture(lecturer1, 'Java', 8))     # Ошибка (лектор не ведёт Java)
print(student1.rate_lecture(lecturer2, 'Java', 7))     # None
print(student2.rate_lecture(lecturer1, 'C++', 10))     # None
print(student2.rate_lecture(lecturer2, 'Python', 8))   # None

# 2. Ревьюеры оценивают домашние задания студентов
print(reviewer1.rate_hw(student1, 'Python', 8))        # None
print(reviewer1.rate_hw(student1, 'Java', 9))          # None
print(reviewer2.rate_hw(student2, 'Python', 7))        # None
print(reviewer2.rate_hw(student2, 'C++', 10))          # None
print(reviewer1.rate_hw(student2, 'Java', 6))          # Ошибка (студент2 не изучает Java)

# 3. Добавление завершённых курсов студентам
student1.add_courses('Введение в программирование')
student2.add_courses('Алгоритмы и структуры данных')

# 4. Вывод информации через __str__
print("\n=== Студенты ===")
print(student1)
print()
print(student2)

print("\n=== Лекторы ===")
print(lecturer1)
print()
print(lecturer2)

print("\n=== Ревьюеры ===")
print(reviewer1)
print()
print(reviewer2)

# ========== Вызов функций подсчёта средних оценок ==========
students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]

print("\n=== Средние оценки ===")
print(f"Средняя оценка за ДЗ по курсу Python: {average_hw_grade(students_list, 'Python'):.2f}")
print(f"Средняя оценка за ДЗ по курсу Java: {average_hw_grade(students_list, 'Java'):.2f}")
print(f"Средняя оценка за ДЗ по курсу C++: {average_hw_grade(students_list, 'C++'):.2f}")

print(f"Средняя оценка за лекции по курсу Python: {average_lecture_grade(lecturers_list, 'Python'):.2f}")
print(f"Средняя оценка за лекции по курсу Java: {average_lecture_grade(lecturers_list, 'Java'):.2f}")
print(f"Средняя оценка за лекции по курсу C++: {average_lecture_grade(lecturers_list, 'C++'):.2f}")