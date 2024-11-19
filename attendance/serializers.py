from rest_framework import serializers
from .models import Attendance
from courses.models import *
class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Attendance
        fields = ('id', 'student', 'course', 'date', 'status')
    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        print(f"Validating: Student={student}, Course={course}")
        print("Enrollment QuerySet:", Enrollment.objects.filter(student=student, course=course))
        if not Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Студент не зарегистрирован на данный курс.")

        return data