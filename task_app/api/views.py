from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import TaskUserSerializer, TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardMember
from django.db.models import Q
from task_app.models import Task
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
    permission_classes = [IsAuthenticated, IsBoardMember]
    serializer_class = TaskUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(board__owner=user) | Q(board__members=user)
        ).distinct()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # ruft check_object_permissions auf
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Response immer im GET-Format
        return Response(
            TaskSerializer(instance, context={"request": request}).data,
            status=status.HTTP_200_OK
        )
    


