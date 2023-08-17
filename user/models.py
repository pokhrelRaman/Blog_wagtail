from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    profilePicture = models.ImageField(default="") 
    personalInformation = models.CharField(null=True,max_length=200) 
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    def __self__(self):
        return str(self.user.first_name)


