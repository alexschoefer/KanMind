from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.board.owner == user
            or obj.board.members.filter(id=user.id).exists()
        )

