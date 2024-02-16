from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    The manager class that swaps a username with an email.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Creates a new user with given credentials."""
        if not email:
            raise ValueError("`%s` is invalid email." % email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a superuser with his password and an email.
        """
        extra_fields.update({
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        })
        return self.create_user(email, password, **extra_fields)


class ContactInformation(models.Model):
    """
    The additional contact information about the user.
    """

    phone_number = PhoneNumberField("User phone number")
    location = models.CharField("Place of residence", max_length=32)

    class Meta:
        verbose_name = 'Contact information'
        verbose_name_plural = 'Contact information'


class CustomUser(AbstractUser):
    """
    The custom user model. Swaps an email with a username field.
    """

    email = models.EmailField('Email', unique=True)
    username = models.CharField('Username', max_length=16, validators=[UnicodeUsernameValidator()])
    contact_info = models.OneToOneField(
        ContactInformation, on_delete=models.CASCADE, verbose_name="User profile",
        related_name='user', null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
