from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):

    #Repeated Password nur schreiben, aber nicht zurückgeben
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 
            'fullname', 
            'password', 
            'repeated_password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    #Password Validierung
    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Your passwords do not match. Please try again."})
        return data
    
    #Email Validierung
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email address already belongs to an account.')
        return value
    
    #Create User
    def create(self, validated_data):
        repeated_password = validated_data.pop('repeated_password')
        fullname = validated_data.pop('fullname')
        email = validated_data['email']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, fullname=fullname)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = self._get_user_by_email(email)
        self._check_password(user, password)

        data['user'] = user
        return data

    def _get_user_by_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'No account with this email address.'
            })

    def _check_password(self, user, password):
        if not authenticate(username=user.username, password=password):
            raise serializers.ValidationError({
                'password': 'Invalid password. Please check.'
            })

    
