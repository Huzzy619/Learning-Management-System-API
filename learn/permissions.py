from email import message
from rest_framework import permissions


class IsMentor (permissions.BasePermission):

    message = "You have to be a Mentor to create, update, or delete"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_mentor)

class IsStudent(permissions.BasePermission):
    message = "Only Students can give answers to tasks"

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(request.user.is_authenticated and not request.user.is_mentor)

        return bool(request.user.is_authenticated or request.user.is_mentor)