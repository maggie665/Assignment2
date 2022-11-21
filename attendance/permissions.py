
from rest_framework import permissions


class IsLecturerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.lecturer == request.user


class IsLecturer(permissions.BasePermission):
    message = "You are not a lecturer"

    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list("name", flat=True)
        if "lecturer" in user_groups:
            return True
        return False