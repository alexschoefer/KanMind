from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from board_app.models import Board
from .serializers import (
    BoardDashboardSerializer,
    BoardCreateSerializer,
    BoardUpdateSerializer,
    BoardUpdateResponseSerializer,
    EmailCheckSerializer,
    SingleBoardDetailSerializer
)
from .permissions import IsBoardMemberOrOwner, IsBoardOwner


class BoardDashboardView(generics.ListCreateAPIView):
    """
    API view for listing and creating boards.

    Returns boards where the authenticated user is either
    the owner or a member.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BoardDashboardSerializer

    def get_queryset(self):
        """
        Return all boards owned by or shared with the user.

        :raises PermissionDenied: If the user is not authenticated
        """
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied(
                "You must be logged in to view boards."
            )

        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on request method.
        """
        if self.request.method == "POST":
            return BoardCreateSerializer
        return BoardDashboardSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new board and return dashboard representation.
        """
        serializer = self.get_serializer(
                    data=request.data,
                    context={"request": request},
                )
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        dashboard_serializer = BoardDashboardSerializer(
                    board,
                    context={"request": request},
                )

        return Response(
                    dashboard_serializer.data,
                    status=status.HTTP_201_CREATED,
                )


class SingleBoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single board.

    Access is restricted based on board membership and ownership.
    """

    queryset = Board.objects.all()
    serializer_class = SingleBoardDetailSerializer

    def get_permissions(self):
        """
        Return permissions based on request method.

        - DELETE: Only board owner
        - GET / PATCH / PUT: Board members or owner
        """
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]
    

    def patch(self, request, *args, **kwargs):
        """
        Partially update a board and return the updated board data.
        """
        instance = self.get_object()

        serializer = BoardUpdateSerializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = BoardUpdateResponseSerializer(
            instance,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class EmailCheckView(APIView):
    """
    API view for checking whether an email address
    is associated with an existing user account.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Validate the provided email address and return user data
        if the email exists.
        """
        serializer = EmailCheckSerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            fullname = (
                f"{user.first_name} {user.last_name}".strip()
                or user.username
            )

            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "fullname": fullname,
                }
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "Email not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
