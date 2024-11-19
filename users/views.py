# users/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role
from django.views import View
from django.shortcuts import render
from .serializers import UserSerializer, UserCreateSerializer, RoleSerializer
import logging

logger = logging.getLogger('custom_logger')


class RegisterPageView(View):
    def get(self, request):
        logger.info(f"User on page register.html")
        return render(request, 'users/register.html')


class LoginPageView(View):
    def get(self, request):
        logger.info(f"User on page login.html")
        return render(request, 'users/login.html')


class RoleAssignView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, user_id, role_id):
        try:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
            user.role = role
            user.save()

            # Логируем успешное назначение роли
            logger.info(f"Role assigned: {role.name} to User {user.username} (ID: {user_id})")

            return Response({"status": "role assigned"})
        except User.DoesNotExist:
            # Логируем, если пользователь не найден
            logger.error(f"Failed to assign role: User with ID {user_id} does not exist.")
            return Response({"error": "User not found"}, status=404)
        except Role.DoesNotExist:
            # Логируем, если роль не найдена
            logger.error(f"Failed to assign role: Role with ID {role_id} does not exist.")
            return Response({"error": "Role not found"}, status=404)
        except Exception as e:
            # Логируем любую другую ошибку
            logger.error(f"Failed to assign role: {str(e)}")
            return Response({"error": "An error occurred"}, status=500)

