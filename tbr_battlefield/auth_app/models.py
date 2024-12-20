from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, mobile, password, **extra_fields)

# Abstract User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('coach', 'Coach'),
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # For Django Admin access

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email









class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return f"Admin: {self.user.name}"

class CoachProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='coach_profile')
    experience = models.IntegerField()
    bio = models.TextField()

    def __str__(self):
        return f"Coach: {self.user.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')

    def __str__(self):
        return f"User: {self.user.name}"
