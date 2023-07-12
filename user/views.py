from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserProfileSerializer,UserRegistrationSerializer,UpdateUserDetailsSerializer, UpdatePasswordSerializer, UserEmailVerificatonSerializer, RequestResetPasswordSerializer,ResetPasswordSerializer

from customlib.views.views import PutAPIView

#for auth
from django.utils.encoding import smart_str,force_bytes
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator,PasswordResetTokenGenerator


#for Swagger
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    @swagger_auto_schema(
        request_body= UserRegistrationSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def post(self,request):
        serializer = UserRegistrationSerializer(data= request.data)
        
        if serializer.is_valid():            
            user = serializer.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return Response({"uid":uid ,"token":token})
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST )
    

class EmailVerification(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_class = [IsAuthenticated]

    serializer_class = UserEmailVerificatonSerializer
    @swagger_auto_schema(
    request_body= UserEmailVerificatonSerializer,
    responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def post(self,request):
        serializer = UserEmailVerificatonSerializer
        if serializer.is_valid():
            uid = request.body.get('uid')
            token = request.body.get('token')
            uid = urlsafe_base64_decode(uid).decode()
            
            try:
                user = User.objects.get(uid)
                if user and default_token_generator.check_token(user,token):
                    user.is_active = True
                    return Response({'msg':'user verified'})
                return Response({'msg':'invalid token provided'}, status= status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'msg':'User not found'}, status= status.HTTP_404_NOT_FOUND)

    
class UserUpdateView(PutAPIView):
    authentication_classes = [JWTAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = UpdateUserDetailsSerializer
    
    @swagger_auto_schema(
        request_body= UpdateUserDetailsSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def put(self,request):
        user = request.user
        print(user)
        serializer = UpdateUserDetailsSerializer(instance= user, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'User updated'})
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST )
    

class ChangePasswordView(PutAPIView):
    permission_class = [AllowAny]

    serializer_class = UpdatePasswordSerializer
    @swagger_auto_schema(
    request_body= UpdatePasswordSerializer,
    responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def put(self,request):
        user = request.user
        serializer = UpdatePasswordSerializer(request.data)
        if serializer.is_valid():
            if user.check_password(request.data.get('oldPassword')):
                user.set_password(request.data.get('newPassword'))
                user.save()
                serializer.save()
            return Response({'msg':'password is incorrect'})
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    
class ResetPasswordRequestView(CreateAPIView):
    permission_class = [AllowAny]

    serializer_class = RequestResetPasswordSerializer
    @swagger_auto_schema(
    request_body= RequestResetPasswordSerializer,
    responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    
    def create(self,request):
        serializer = RequestResetPasswordSerializer(request.data)
        if serializer.is_valid():
            if User.objects.filter(email = request.data.get('email')).exists():
                user = User.objects.get(email = request.data.get('email'))
                uid = user.id
                uid = urlsafe_base64_encode(force_bytes(uid))
                token = PasswordResetTokenGenerator().make_token(user= user)
                link = f"http://localhost:8000/auth/v1.0/reset/{uid}/{token}"
                print(link)
                return Response({'uid':uid,'token':token})
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self,request):
        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():
            uid = request.data.get('uid')
            token = request.data.get('token')
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(id = uid)
            if user and default_token_generator.check_token(user,token):
                user.set_password(request.data['password'])
                return Response({'message':"Resetting password was successful"},status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            token = RefreshToken.for_user(request.user)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


#  register, verify ,  update , resetpassword, change password , login , logout