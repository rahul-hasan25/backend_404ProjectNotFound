from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id'             : self.user.id,
            'email'          : self.user.email,
            'username'       : self.user.username,
            'role'           : self.user.role,
            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None
        }
        return data
    
class UserRegisterSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})
    profile_picture  = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model  = User
        fields = ['full_name', 'email', 'password', 'confirm_password', 'profile_picture']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        profile_picture = validated_data.pop('profile_picture', None)
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            role='annotator'
        )
        
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        
        try:
            user = User.objects.get(email=username)
            attrs["username"] = user.username  
        except User.DoesNotExist:
            pass
            
        data = super().validate(attrs)
        
        data['user'] = {
            'id'      : self.user.id,
            'email'   : self.user.email,
            'username': self.user.username
        }
        return data
    
    

# Forget Password Serializer
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No operator account registered with this email.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    uidb64           = serializers.CharField()
    token            = serializers.CharField()
    password         = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        try:
            uid  = urlsafe_base64_decode(data['uidb64']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"token": "Invalid or corrupted user identifier."})

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError({"token": "The reset link has expired or is invalid."})

        data['user'] = user
        return data