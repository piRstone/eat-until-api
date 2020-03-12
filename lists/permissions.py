from rest_framework import permissions


class ListPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Only the owned can perform write operations"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user
