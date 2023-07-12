from django.urls import path,include
from .views import UserRegistrationView,UserUpdateView,ChangePasswordView,ResetPasswordRequestView,ResetPasswordView,EmailVerification,LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   



urlpatterns = [
    path('userRegistration',UserRegistrationView.as_view()),
    path('emailVerification',EmailVerification.as_view()),
    path('userUpdate',UserUpdateView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='loginPage'),
    path('refreshToken', TokenRefreshView.as_view(), name='token_refresh'),
    path('changePassword',ChangePasswordView.as_view()),
    path('resetPassword',ResetPasswordView.as_view()),
    path('requestResetPassword',ResetPasswordRequestView.as_view()),
    path('logout',LogoutView.as_view()),
    path('blog/',include('blogmain.urls'))
] 

#  register, verify ,  update , resetpassword, change password , login , logout