from .serializers import RegistrationSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken


def create_auth_token_response(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'fullname': user.userprofile.fullname,
        'email': user.email,
        'user_id': user.id
    }

class RegistrationView(generics.CreateAPIView):
    #Alles zu lassen
    permission_classes = [AllowAny]

    serializer_class = RegistrationSerializer

    def get(self, request):
        return Response({'message': 'running...'}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        # Serializer initialisieren
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2User erstellen (kommt aus serializer.create())
        user = serializer.save()

        # Token + User-Daten zurückgeben
        response_data = create_auth_token_response(user)

        # HTTP 201 Created
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        response_data = create_auth_token_response(user)
        return Response(response_data, status=status.HTTP_200_OK)

