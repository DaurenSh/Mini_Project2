from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsAdminOrIsTeacher
import logging

logger = logging.getLogger('custom_logger')

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrIsTeacher]

    def perform_create(self, serializer):
        # Автоматическое назначение текущего пользователя как teacher
        serializer.save(teacher=self.request.user)
        logger.info(f"Grade created: Student {serializer.instance.student.name}, Course {serializer.instance.course.name}, Grade {serializer.instance.grade}")