from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.

    Handles validation of email uniqueness, password confirmation
    and creation of the User and related UserProfile.
    """
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

    def validate(self, data):
        """
        Validate that password and repeated_password match.

        :param data: Incoming validated data
        :return: Validated data
        :raises ValidationError: If passwords do not match
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Your passwords do not match. Please try again."})
        return data
    
    def validate_email(self, value):
        """
        Validate that the email address is unique.

        :param value: Email address
        :return: Email address
        :raises ValidationError: If email already exists
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email address already belongs to an account.')
        return value
    
    def create(self, validated_data):
        """
        Create a new user and associated user profile.

        :param validated_data: Validated serializer data
        :return: Created User instance
        """
        validated_data.pop('repeated_password')
        fullname = validated_data.pop('fullname')
        email = validated_data['email']

        user = User.objects.create_user(
            username=fullname,
            email=email,
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, fullname=fullname)
        return user


class UserLoginSerializer(serializers.Serializer):

    """
    Serializer for user authentication using email and password.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate user credentials.

        :param data: Incoming login data
        :return: Validated data with user instance
        :raises ValidationError: If credentials are invalid
        """

        email = data.get('email')
        password = data.get('password')

        user = self._get_user_by_email(email)
        self._check_password(user, password)

        data['user'] = user
        return data

    def _get_user_by_email(self, email):
        """
        Retrieve a user by email address.

        :param email: Email address
        :return: User instance
        :raises ValidationError: If user does not exist
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'No account with this email address.'
            })

    def _check_password(self, user, password):
        """
        Check if the provided password is correct. 
        If password is invalid, a ValidationError is given
        """
        if not authenticate(username=user.username, password=password):
            raise serializers.ValidationError({
                'password': 'Invalid password. Please check.'
            })

    
