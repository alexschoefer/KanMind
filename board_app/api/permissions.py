from rest_framework import permissions

class IsBoardMemberOrOwner(permissions.BasePermission):
    """
    Permission class that allows access only to board members or the board owner.

    This permission is evaluated both on the view level (authentication check)
    and on the object level (ownership or membership check).
    """

    def has_permission(self, request, view):
        """
        Check whether the user is authenticated.
        Args:
            request: The HTTP request object.
            view: The view being accessed.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is allowed to access the given board.

        A user is allowed access if they are either:
        - the owner of the board, or
        - a member of the board.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj (Board): The board instance being accessed.

        Returns:
            bool: True if the user is the owner or a member of the board.
        """
        user = request.user
        return (
            obj.owner_id == user.id
            or obj.members.filter(id=user.id).exists()
        )


class IsBoardOwner(permissions.BasePermission):
    """
    Permission class that allows access only to the board owner.

    This permission is typically used for destructive actions such as
    deleting a board.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is the owner of the board.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj (Board): The board instance being accessed.

        Returns:
            bool: True if the user owns the board, False otherwise.
        """
        return obj.owner == request.user
