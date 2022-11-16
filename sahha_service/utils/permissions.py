from rest_framework import permissions as rest_permissions
from sahha_service import models


class IsActiveUser(rest_permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and hasattr(request.user,"sahha_service"):
            return request.user.is_active