from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import date
from django.core.validators import (
    FileExtensionValidator
)
from django.db.models import Q

# --------------------- MODELS ----------------------
class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User.
        """
        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    TYPE_CHOICES = (
        ('builder', 'builder'),
        ('dealer', 'dealer'),
        ('owner', 'owner'),
    )

    objects = CustomUserManager()
    type_of_user = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=False,
        null=False,
    )

    def __str__(self):
        return str(self.username)

# Property dealer client
class LinkedAccounts(models.Model):
    site_choices = (
            ('olx', 'olx'),
            ('bricks', 'bricks'),            
        )
    email = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
    site = models.CharField(
        max_length=20,
        choices=site_choices,
        blank=False,
        null=False,
    )
    auth_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return str(self.email) + ' ' + str(self.site)
        