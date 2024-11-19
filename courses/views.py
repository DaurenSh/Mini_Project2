from rest_framework import viewsets, permissions
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsAdminOrIsTeacher
from django_filters import rest_framework as filters
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# Логгер
logger = logging.getLogger('custom_logger')
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        enrollment = serializer.save()

        # Логирование регистрации на курс
        logger.info(f"Enrollment created: Student {enrollment.student.name} -> Course {enrollment.course.name}")

class CourseFilter(filters.FilterSet):
    instructor = filters.NumberFilter(field_name="instructor_id")

    class Meta:
        model = Course
        fields = ['instructor']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAdminOrIsTeacher]
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()

        # Логирование информации о создании курса
        logger.info(
            f"Course created: {course.name}, Instructor: {course.instructor.username if course.instructor else 'None'}")

    @method_decorator(cache_page(60 * 5))  # Кэш на 5 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)