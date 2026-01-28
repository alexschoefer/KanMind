from rest_framework import permissions
from board_app.models import Board


class IsBoardMemberOrOwner(permissions.BasePermission):

    # def has_object_permission(self, request, view, obj: Board):
    #     return obj.owner == request.user or request.user in obj.members.all()

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.owner_id == user.id
            or obj.members.filter(id=user.id).exists()
        )

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
