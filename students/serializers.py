from rest_framework import serializers

from courses.models import Course
from .models import Student
from django.contrib.auth import get_user_model
User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Student
        fields = ('user_id', 'name', 'email', 'dob', 'registration_date')

    def create(self, validated_data):
        # Извлекаем user из validated_data и передаем его в Student
        user = validated_data.pop('user')
        student = Student.objects.create(user=user, **validated_data)
        return student

class NestedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class StudentWithCoursesSerializer(serializers.ModelSerializer):
    courses = NestedCourseSerializer(many=True, source='enrollments.course')

    class Meta:
        model = Student
        fields = ['id', 'name', 'courses']


from rest_framework import serializers
from .models import Student
from courses.models import Course, Enrollment
from grades.models import Grade
from attendance.models import Attendance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description']

class GradeSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Grade
        fields = ['course', 'grade', 'date']

class AttendanceSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Attendance
        fields = ['course', 'date', 'status']

class StudentProfileSerializer(serializers.ModelSerializer):
    # Включаем курсы, на которые записан студент, его оценки и посещаемость
    courses = CourseSerializer(source='enrollments.course', many=True)
    grades = GradeSerializer(many=True, source='grades')
    attendance_records = AttendanceSerializer(many=True, source='attendance_records')

    class Meta:
        model = Student
        fields = ['name', 'email', 'dob', 'courses', 'grades', 'attendance_records']
