from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings # Needed for settings.AUTH_USER_MODEL reference
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import check_password
from Project.models import Project

class User(AbstractUser):

    # Custom fields added to the core User model
    country_origin = models.CharField(max_length=50, blank=False, default='')
    email = models.EmailField(blank=False, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    identity_number = models.CharField(max_length=255, unique=True, null=False, blank=False)
    
    # NOTE: profilePicture renamed to profile_picture (snake_case convention)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

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

    def check_identity_number(self, raw_identity_number):
        return check_password(raw_identity_number, self.identity_number)

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
    hourly_rate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True )
    #         validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]),
    avatar = models.ImageField(blank=True)
    
    class SkillLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        JUNIOR = 'junior', 'Junior'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        SENIOR = 'senior', 'Senior'
        EXPERT = 'expert', 'Expert'
        
        # Field to store the user's skill level for the module
    level = models.CharField(max_length=20,
    choices=SkillLevel.choices,
    # Set the default to the lowest tier: 'beginner'
    default=SkillLevel.BEGINNER,
    verbose_name="Module Skill Level"
)     
        

    
    class Availability(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        NOT_AVAILABLE = 'NOT_AVAILABLE', 'Not Available'
        
    availability = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE
    )

def __str__(self):
        return f"{self.user.username}'s Profile ({self.get_role_display()})"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Payment of {self.amount} for {self.project.title} by {self.user.username} via {self.get_payment_method_display()}"