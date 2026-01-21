from rest_framework import serializers
from auth_app.models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):

    #Repeated Password nur schreiben, aber nicht zurückgeben
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user_email', 
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
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email address already belongs to an account.')
        return value
    
    #Create User
    def create(self, validated_data):

        #Passwort ist nur für die Validation notwendig, keine Speicherung 
        validated_data.pop('repeated_password')

        user = UserProfile.objects.create_user(
        username=validated_data['username'],
        email=validated_data.get('email'),
        password=validated_data['password']
        )

        return user
