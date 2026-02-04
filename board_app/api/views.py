from .serializers import BoardDashboardSerializer, BoardCreateSerializer, EmailCheckSerializer, BoardUpdateSerializer, BoardUpdateResponseSerializer
from board_app.models import Board
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardMemberOrOwner, IsBoardOwner
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User


class BoardDashboardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
    
class SingleBoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = BoardUpdateSerializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = BoardUpdateResponseSerializer(
            instance,
            context={"request": request}
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = EmailCheckSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            fullname = f"{user.first_name} {user.last_name}".strip() or user.username
            return Response({
                "id": user.id,
                "email": user.email,
                "fullname": fullname
            })
        except User.DoesNotExist:
            return Response(
                {"detail": "Email not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    
