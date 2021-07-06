from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsOwnerOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not IsAuthenticated.has_permission(self, request, view):
            return False
        if request.user and request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

