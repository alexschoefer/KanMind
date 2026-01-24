from .serializers import BoardDashboardSerializer
from board_app.models import Board
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

class BoardDashboardView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardDashboardSerializer

    #gib mir die Boards, die der Benutzer erstellt hat ODER Mitglied ist
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view boards.")
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    