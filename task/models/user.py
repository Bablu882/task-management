from enum import unique
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, PermissionsMixin):
    last_name = None
    last_login = None
    date_joined = None
    first_name = None
    username = None

    USERNAME_FIELD = 'number'

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=254)
    created_on = models.DateTimeField(auto_now_add=True)