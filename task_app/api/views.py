from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import TaskUserSerializer, TaskSerializer, TaskCreateSerializer
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

    


