from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView 
from .views import *

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='auth_signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    
    path('me/', UserProfileView.as_view(), name='user_profile'),
]