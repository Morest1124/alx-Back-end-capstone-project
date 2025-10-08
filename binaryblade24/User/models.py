from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings # Needed for settings.AUTH_USER_MODEL reference


class User(AbstractUser):

    # Custom fields added to the core User model
    country_origin = models.CharField(max_length=50, blank=False, default='')
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    identity_number = models.CharField(max_length=255, unique=True, null=False, blank=False)
    
    # NOTE: profilePicture renamed to profile_picture (snake_case convention)
    # profile_picture = models.ImageField(blank=True, null=True) 

    # Use 'email' for login:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country_origin'] 

    # Field overrides (required to avoid Django's default User model conflicts in a custom user model setup)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    
    # One-to-One link to User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Define User Roles
    class UserRoles(models.TextChoices):
        # NOTE: Removed leading space from ' FREELANCER'
        ADMIN = 'ADMIN','Admin'
        CLIENT = 'CLIENT', 'Client'
        FREELANCER = 'FREELANCER', 'Freelancer' 
        
    # Field to store the role
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.FREELANCER 
    )
    
    # Other non-identity profile fields
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.get_role_display()})"