from .serializers import BoardDashboardSerializer, BoardCreateSerializer
from board_app.models import Board
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardMemberOrOwner
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied


class BoardDashboardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
    serializer_class = BoardDashboardSerializer

    #gib mir die Boards, die der Benutzer erstellt hat ODER Mitglied ist
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view boards.")
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    
    #prüfe ob GET oder POST
    def get_serializer_class(self):
        if self.request.method == "POST":
            return BoardCreateSerializer
        return BoardDashboardSerializer
    
class BoardCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        self.board = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        dashboard_serializer = BoardDashboardSerializer(
            self.board,
            context={"request": request}
        )
        return Response(dashboard_serializer.data, status=status.HTTP_201_CREATED)
