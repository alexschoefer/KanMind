from rest_framework import generics
from .serializers import TaskUserSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
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
    


