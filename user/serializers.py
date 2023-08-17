from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['first_name','last_name','username']


class UserProfileSerializer(serializers.ModelSerializer):
    profilePicture = serializers.ImageField(required = False)
    user = UserSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ['id','user','profilePicture','personalInformation']
    
    def create(self,data):
        userProfile = UserProfile.objects.create(
                                                    user = self.context.get('user'),
                                                    profilePicture = data.get('profilePicture'),
                                                    personalInformation = data.get('personalInformation')
                                                )
        return userProfile

    def update(self,instance,data):
        instance.profilePicture
        instance.personalInformation
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

    def create(self,data):
        user = User.objects.create(
                                    first_name = data.get('first_name'),
                                    last_name = data.get('last_name'),
                                    username = data.get('username'),
                                    email = data.get('email'), 
                                    )
        user.set_password(data['password'])
        user.is_active = False
        user.save()
        return user
    
class UserEmailVerificatonSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length = 200)
    token = serializers.CharField(max_length = 200)


class UpdateUserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 20) 
    last_name = serializers.CharField(max_length = 20)
    username =  serializers.CharField(max_length = 20)
    class Meta:
        fields = ('first_name','last_name','username')

    def update(self,instance,data):
        instance.first_name = data['first_name']
        instance.last_name = data['last_name']
        instance.username = data['username']
        instance.save()
        return instance

class UpdatePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(max_length = 20)
    newPassword = serializers.CharField(max_length = 20)
    
class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 20)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 200)





