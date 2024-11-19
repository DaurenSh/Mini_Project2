from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from users.permissions import IsStudent
from .models import Student
from .serializers import StudentProfileSerializer, StudentSerializer
import logging

logger = logging.getLogger('custom_logger')

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsStudent]
        return super().get_permissions()

    def perform_create(self, serializer):
        student = serializer.save()

        # Логирование информации о создании студента
        logger.info(
            f"Student created: {student.name}, Email: {student.email}, User: {student.user.username if student.user else 'None'}")


