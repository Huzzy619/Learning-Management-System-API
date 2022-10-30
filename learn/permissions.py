from rest_framework import permissions


class IsMentor (permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_mentor)
