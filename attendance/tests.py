from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Attendance
from students.models import Student
from courses.models import Course, Enrollment
from rest_framework import status

from django.test import TestCase
from users.models import User, Role  # Импорт кастомной модели User
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance

from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class AttendanceModelTest(TestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username="student_user", email="student@example.com",
                                             password="password123")

        # Создание студента и курса
        self.student = Student.objects.create(user=self.user, name="John Doe", email="john@example.com",
                                              dob="2000-01-01")
        self.course = Course.objects.create(name="Math 101", description="Basic Math")

        # Регистрация студента на курс
        Enrollment.objects.create(student=self.student, course=self.course)

    def test_attendance_creation(self):
        attendance = Attendance.objects.create(
            student=self.student,
            course=self.course,
            date="2024-11-12",
            status="Present"
        )
        self.assertEqual(attendance.student.name, "John Doe")
        self.assertEqual(attendance.course.name, "Math 101")
        self.assertEqual(attendance.status, "Present")


class AttendanceAPITest(APITestCase):
    def setUp(self):
        # Создание ролей
        self.teacher_role = Role.objects.create(name="Teacher", description="Can manage attendance and grades")
        self.student_role = Role.objects.create(name="Student", description="Can view own records")

        # Создание пользователей
        self.user = User.objects.create_user(username="student_user", email="student@example.com",
                                             password="password123", role=self.student_role)
        self.teacher = User.objects.create_user(username="teacher_user", email="teacher@example.com",
                                                password="password123", role=self.teacher_role)

        # Создание студента и курса
        self.student = Student.objects.create(user=self.user, name="John Doe", email="john@example.com",
                                              dob="2000-01-01")
        self.course = Course.objects.create(name="Math 101", description="Basic Math")

        # Создание регистрации студента на курс
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)

        # Отладка идентификаторов
        print(f"Student ID: {self.student.id}, Course ID: {self.course.id}")
        print(f"Enrollment created: {self.enrollment}")

        # Данные для теста
        self.attendance_data = {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-11-12",
            "status": "Present"
        }
        print("Attendance Data:", self.attendance_data)

        # Получение токена для учителя
        self.teacher_token = get_token_for_user(self.teacher)

    def test_create_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")
        response = self.client.post("/attendance/", self.attendance_data)
        if response.status_code == 400:
            print("Response errors:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)

    def test_unauthorized_access(self):
        self.client.credentials()  # Удаляем токен для эмуляции неавторизованного пользователя
        response = self.client.post("/attendance/", self.attendance_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)