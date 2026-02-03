from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import TaskUserSerializer, TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskUpdateResponseSerializer, TaskCommentCreateSerializer, TaskCommentsSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardMember, IsTaskCreatorOrBoardOwner
from django.db.models import Q
from task_app.models import Task, TaskCommentModel
from board_app.models import Board

class TasksAssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
            assignee=user
        ).filter(
            Q(board__members=user) | Q(board__owner=user)
        ).distinct()
    
class TasksReviewedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
            reviewer=user
        ).filter(
            Q(board__members=user) | Q(board__owner=user)
        ).distinct()
    
class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        self.task = serializer.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            TaskSerializer(self.task, context={"request": request}).data,
            status=status.HTTP_201_CREATED
        )

class SingleTaskView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return TaskUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # check_object_permissions()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            TaskUpdateResponseSerializer(
                instance,
                context={"request": request}
            ).data,
            status=status.HTTP_200_OK
        )

    
class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        return TaskCommentModel.objects.filter(
            task_id=self.kwargs["pk"]
        ).select_related("author__userprofile").order_by("created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCommentCreateSerializer
        return TaskCommentsSerializer

    def perform_create(self, serializer):
        serializer.save(
            task_id=self.kwargs["pk"],
            author=self.request.user
        )


