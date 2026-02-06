from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegistrationSerializer, UserLoginSerializer


def create_auth_token_response(user):
    """
    Create a standardized authentication response payload.

    Generates or retrieves an authentication token for the given user
    and returns basic user information.

    :param user: Authenticated user instance
    :return: Dictionary containing token and user data
    """
    token, _ = Token.objects.get_or_create(user=user)
    return {
        "token": token.key,
        "fullname": user.userprofile.fullname,
        "email": user.email,
        "user_id": user.id,
    }


class RegistrationView(generics.CreateAPIView):
    """
    API view for user registration.

    Allows anonymous users to register and returns
    an authentication token upon successful creation.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def get(self, request):
        """
        Health check endpoint for the registration view.
        """
        return Response(
            {"message": "running..."},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        """
        Handle user registration.

        Validates incoming data, creates a new user,
        and returns an authentication token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        response_data = create_auth_token_response(user)

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )


class CustomLoginView(ObtainAuthToken):
    """
    API view for user authentication using email and password.

    Returns an authentication token and basic user information
    upon successful login.
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        Authenticate the user and return an auth token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        response_data = create_auth_token_response(user)

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )
