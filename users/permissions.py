from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"Usuario autenticado: {request.user}")
        return request.user.is_authenticated and request.user.role == 1