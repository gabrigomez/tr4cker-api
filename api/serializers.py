from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Artist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', 'image', 'genre', 'user', 'id', 'spotify_id')

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Usuário não cadastrado!',
        'invalid_credentials': 'Senha incorreta!',
    }

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(self.error_messages['no_active_account'], code='no_active_account')

        if not user.check_password(password):
            raise serializers.ValidationError(self.error_messages['invalid_credentials'], code='invalid_credentials')

        return super().validate(attrs)
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token