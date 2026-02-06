from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from board_app.models import Board
from task_app.models import Task, TaskCommentModel

from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskUpdateResponseSerializer,
    TaskCommentCreateSerializer,
    TaskCommentsSerializer,
)
from .permissions import (
    IsBoardMember,
    IsTaskCreatorOrBoardOwner,
    IsCommentAuthor,
)


class TasksAssignedToMeView(generics.ListAPIView):
    """
    API view for listing tasks assigned to the authenticated user.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return tasks assigned to the user within boards
        where the user is a member or owner.
        """
        user = self.request.user

        return Task.objects.filter(
            assignee=user
        ).filter(
            Q(board__members=user) | Q(board__owner=user)
        ).distinct()


class TasksReviewedToMeView(generics.ListAPIView):
    """
    API view for listing tasks where the authenticated user
    is assigned as reviewer.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return tasks reviewed by the user within boards
        where the user is a member or owner.
        """
        user = self.request.user

        return Task.objects.filter(
            reviewer=user
        ).filter(
            Q(board__members=user) | Q(board__owner=user)
        ).distinct()


class TaskCreateView(generics.CreateAPIView):
    """
    API view for creating a new task.
    """

    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the created task instance for response serialization.
        """
        self.task = serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Create a task and return the full task representation.
        """
        super().create(request, *args, **kwargs)

        return Response(
            TaskSerializer(
                self.task,
                context={"request": request},
            ).data,
            status=status.HTTP_201_CREATED,
        )


class SingleTaskView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single task.
    """

    queryset = Task.objects.all()

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on request method.
        """
        if self.request.method in ["PATCH", "PUT"]:
            return TaskUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        """
        Return permissions based on request method.

        - DELETE: Task creator or board owner
        - GET / PATCH / PUT: Board members
        """
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]

    def patch(self, request, *args, **kwargs):
        """
        Partially update a task and return updated task data.
        """
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            TaskUpdateResponseSerializer(
                instance,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating comments for a task.
    """

    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        """
        Return all comments for the given task ordered by creation date.
        """
        return TaskCommentModel.objects.filter(
            task_id=self.kwargs["pk"]
        ).select_related(
            "author__userprofile"
        ).order_by("created_at")

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on request method.
        """
        if self.request.method == "POST":
            return TaskCommentCreateSerializer
        return TaskCommentsSerializer

    def perform_create(self, serializer):
        """
        Create a new comment associated with the given task.
        """
        serializer.save(
            task_id=self.kwargs["pk"],
            author=self.request.user,
        )


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a task comment.
    """

    queryset = TaskCommentModel.objects.all()
    serializer_class = TaskCommentsSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_queryset(self):
        """
        Return the specific comment for the given task and comment IDs.
        """
        task_id = self.kwargs.get("task_id")
        comment_id = self.kwargs.get("pk")

        return TaskCommentModel.objects.filter(
            task_id=task_id,
            pk=comment_id,
        )
