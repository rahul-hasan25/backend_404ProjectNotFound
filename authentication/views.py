from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes     = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully with profile picture.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "profile_picture": user.profile_picture.url if user.profile_picture else None
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class   = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny] 
    
    
    
# Forget Password API
class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email  = serializer.validated_data['email']
            user   = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token  = default_token_generator.make_token(user)
            
            reset_link = f"http://localhost:3000/reset-password?uid={uidb64}&token={token}"
            
            subject = "404 Workspace - Security Clearance Reset Request"
            message = f"""Hello Operator,

            You requested a security clearance (password) reset for your 404 Workspace account.
            Click the secure link below to proceed with setting up a new master password:

            {reset_link}

            Note: This link will expire shortly for security compliance. If you did not request this, please secure your terminal immediately.

            System Administration,
            404 Workspace Engine.
        """
            try:
                send_mail(subject, message, None, [email])
                return Response({"message": "Secure reset link dispatched to terminal email."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": "Mail delivery subsystem error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user         = serializer.validated_data['user']
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password Reset Successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_picture_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
        
        return Response({
            'full_name'      : user.full_name,
            'profile_picture': profile_picture_url
        })