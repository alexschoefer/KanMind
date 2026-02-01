from rest_framework import permissions
from rest_framework.exceptions import NotFound
from django.db import models
from task_app.models import Task

class IsBoardMember(permissions.BasePermission):
    """
    Prüft, ob der angemeldete User Mitglied oder Owner des Boards ist,
    auf dem der Task liegt.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj ist ein Task
        user = request.user
        board = obj.board  # Board vom Task
        return board.owner == user or board.members.filter(id=user.id).exists()
    
class IsTaskCreatorOrBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.created_by == user
            or obj.board.owner == user
        )