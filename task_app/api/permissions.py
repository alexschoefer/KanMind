from rest_framework import permissions
from task_app.models import Task

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
    

class IsBoardMemberForComment(permissions.BasePermission):
    """
    Allows creating comments only if the user is a member
    or owner of the board the task belongs to.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        task_id = view.kwargs.get("pk")
        if not task_id:
            return False

        try:
            task = Task.objects.select_related("board").get(pk=task_id)
        except Task.DoesNotExist:
            return False

        board = task.board
        user = request.user

        return (
            board.owner == user
            or board.members.filter(id=user.id).exists()
        )
