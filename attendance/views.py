from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsAdminOrIsTeacher
import logging

logger = logging.getLogger('custom_logger')

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrIsTeacher]

    def perform_create(self, serializer):
        attendance = serializer.save()

        # Логирование посещаемости
        logger.info(
            f"Attendance marked: Student {attendance.student.name}, Course {attendance.course.name}, Status {attendance.status}")
