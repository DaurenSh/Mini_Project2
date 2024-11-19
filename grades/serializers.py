from rest_framework import serializers
from .models import Grade
from courses.models import *

class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id', 'student', 'course', 'grade', 'date', 'teacher')

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        if not Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Студент не зарегистрирован на данный курс.")

        return data
