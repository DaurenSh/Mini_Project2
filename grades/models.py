from django.db import models
from django.conf import settings
from students.models import Student
from courses.models import Course

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    grade = models.CharField(max_length=2)
    date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="assigned_grades")

    def __str__(self):
        return f"{self.student.name} - {self.course.name}: {self.grade}"
