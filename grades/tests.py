from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Role
from students.models import Student
from courses.models import Course, Enrollment
from grades.models import Grade
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


# Тестирование модели Grade
class GradeModelTest(TestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.teacher_user = User.objects.create_user(username="teacher_user", email="teacher@example.com",
                                                     password="password123")
        self.student_user = User.objects.create_user(username="student_user", email="student@example.com",
                                                     password="password123")

        # Создание студента и курса
        self.student = Student.objects.create(user=self.student_user, name="John Doe", email="john@example.com",
                                              dob="2000-01-01")
        self.course = Course.objects.create(name="Math 101", description="Basic Math", instructor=self.teacher_user)

        # Регистрация студента на курс
        Enrollment.objects.create(student=self.student, course=self.course)

    def test_grade_creation(self):
        grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            grade="A",
            teacher=self.teacher_user
        )
        self.assertEqual(grade.student.name, "John Doe")
        self.assertEqual(grade.course.name, "Math 101")
        self.assertEqual(grade.grade, "A")
        self.assertEqual(grade.teacher.username, "teacher_user")


# Тестирование API для модели Grade


class GradeAPITest(APITestCase):
    def setUp(self):
        # Создание ролей
        self.teacher_role = Role.objects.create(name="Teacher", description="Can manage grades")
        self.student_role = Role.objects.create(name="Student", description="Can view own grades")

        # Создание пользователей
        self.student_user = User.objects.create_user(username="student_user", email="student@example.com",
                                                     password="password123", role=self.student_role)
        self.teacher_user = User.objects.create_user(username="teacher_user", email="teacher@example.com",
                                                     password="password123", role=self.teacher_role)

        # Создание студента и курса
        self.student = Student.objects.create(user=self.student_user, name="John Doe", email="john@example.com",
                                              dob="2000-01-01")
        self.course = Course.objects.create(name="Math 101", description="Basic Math", instructor=self.teacher_user)

        # Создание регистрации студента на курс
        Enrollment.objects.create(student=self.student, course=self.course)

        # Данные для теста
        self.grade_data = {
            "student": self.student.id,
            "course": self.course.id,
            "grade": "A"
        }

        # Получение токена для учителя
        self.teacher_token = get_token_for_user(self.teacher_user)

    def test_create_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")
        response = self.client.post("/grades/", self.grade_data)
        if response.status_code == 400:
            print("Response errors:", response.data)

        # Проверяем, что оценка создана успешно и поле teacher заполнено
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        grade = Grade.objects.first()
        self.assertEqual(grade.teacher, self.teacher_user)


