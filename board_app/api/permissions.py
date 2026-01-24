from rest_framework import permissions
from board_app.models import Board

class IsBoardMemberOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Board):
        # obj ist hier ein Board-Instanz
        return obj.owner == request.user or request.user in obj.members.all()
