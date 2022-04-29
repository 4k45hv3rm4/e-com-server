from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    """ Custom User Manager for Authenticating user with email number """
    use_in_migrations = True

    def create_user(self,  email, password=None, **extra_fields):
        """Create and save a User with the given Phone number"""
        if not email:
            raise ValueError('User must have Eamil Address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superUser with the given email and name."""

        user = self.create_user(
            email,
            password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserData(AbstractUser):
    """ Table for User Data """
    username = None

    email = models.EmailField(unique=True, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
