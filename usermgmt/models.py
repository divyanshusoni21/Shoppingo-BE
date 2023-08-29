from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from utility.mixins import UUIDMixin
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,  email, password=None,username=''):
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model( email=self.normalize_email(email))
        user.username = username
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user( email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin,UUIDMixin):
    username = models.CharField(max_length=255,blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True,null=True,blank=True)
    phone_no = models.BigIntegerField(unique=True,db_index=True,null=True,blank=True)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True,blank=True)
    last_logout = models.DateTimeField(null=True,blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email 
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }