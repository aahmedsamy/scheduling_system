import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserProfileManager(BaseUserManager):
    """
    Model manager for custom user model UserProfile.
    """

    def create_user(self, email, **kwargs):
        """
        Create a new user with normal privileges.

        Arguments:
            email (str): email of the new user.
        Raises:
            ValueError: When no email is provided.
        Returns:
            user (UserProfile): newly create user object.
        """
        if not email:
            raise ValueError("A user must have an email!")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_unusable_password()
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create a new user with super user privileges.

        Arguments:
            email (str): email of the new user.
            password (str): raw password of the new user
        Returns:
            user (UserProfile): newly create user object.
        """
        user = self.create_user(
            email,
            is_superuser=True,
            is_staff=True,
            #
            first_name="NOT_SET",
            last_name="NOT_SET",
        )

        user.set_password(password)
        user.save()

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user of the system
    """
    email = models.EmailField(max_length=256, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, null=False)
    is_superuser = models.BooleanField(default=False, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = "email"
    objects = UserProfileManager()

    class Meta:
        ordering = ["email"]

    def __str__(self):
        """
        Return string representation for model object.

        Returns:
            (str): string representation using email.
        """
        return str(self.email)
