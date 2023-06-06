from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.CharField(unique=True)
    password = models.CharField()
