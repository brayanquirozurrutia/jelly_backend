import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Los superusuarios deben tener is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    The status choices are:
    - Registered: User is registered but not active (email verification pending)
    - Active: User is active (email verified)
    - Blocked: User is blocked by the administrator (can log in but cannot perform any action)
    - Deleted: User is deleted by the administrator (cannot log in)
    """
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    )
    STATUS_CHOICES = (
        ('R', 'Registered'),
        ('A', 'Active'),
        ('B', 'Blocked'),
        ('D', 'Deleted'),
    )

    password = models.CharField(_('password'), editable=False, blank=False, null=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False, null=False, editable=False)
    rut = models.CharField(max_length=10, default='0', unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(default='0', unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_picture = models.URLField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)
    user_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R', blank=False, null=False)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    user_admin = models.BooleanField(default=False, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'rut',
        'first_name',
        'last_name',
        'gender',
        'password',
    ]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.nickname:
            return self.nickname
        return f"{self.first_name} {self.last_name}"
