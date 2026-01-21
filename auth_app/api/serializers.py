from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User

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
