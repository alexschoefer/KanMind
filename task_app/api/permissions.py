from rest_framework import permissions


class IsBoardMember(permissions.BasePermission):
    """
    Permission class that allows access only to board members or the board owner.

    This permission is used for task-related actions to ensure that only users
    who belong to the board associated with the task can access or modify it.
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
        Check whether the requesting user is a member or the owner of the task's board.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The Task instance being accessed.

        Returns:
            bool: True if the user is the board owner or a board member.
        """
        user = request.user
        board = obj.board
        return board.owner == user or board.members.filter(id=user.id).exists()


class IsTaskCreatorOrBoardOwner(permissions.BasePermission):
    """
    Permission class that allows access only to the task creator or the board owner.

    This permission is typically used for destructive actions such as deleting tasks.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is allowed to modify or delete the task.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The Task instance being accessed.

        Returns:
            bool: True if the user created the task or owns the board.
        """
        user = request.user
        return (
            obj.created_by == user
            or obj.board.owner == user
        )


class IsCommentAuthor(permissions.BasePermission):
    """
    Permission class that allows access only to the author of a comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is the author of the comment.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The TaskComment instance being accessed.

        Returns:
            bool: True if the user authored the comment.
        """
        return obj.author == request.user
