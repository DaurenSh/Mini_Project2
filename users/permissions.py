from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'Student'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'Teacher'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'Admin'

class IsAdminOrIsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role.name == 'Teacher' or request.user.role.name == 'Admin')