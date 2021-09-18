from rest_framework.permissions import BasePermission

class RegisterPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST" or request.user.is_authenticated
