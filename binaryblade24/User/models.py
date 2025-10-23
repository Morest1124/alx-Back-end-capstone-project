from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings # Needed for settings.AUTH_USER_MODEL reference
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import check_password
from Project.models import Project
from django.db.models import Avg

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
    roles = models.ManyToManyField('Role', related_name='users')


    def check_identity_number(self, raw_identity_number):
        return check_password(raw_identity_number, self.identity_number)

    def __str__(self):
        return self.username


class Role(models.Model):
    """Model to represent user roles."""
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    
    # One-to-One link to User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
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
    level = models.CharField(
        max_length=20,
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

    # Computed properties for convenience / API use
    @property
    def completed_projects(self):
        """Return a queryset of this user's completed projects."""
        return Project.objects.filter(client=self.user, status=Project.ProjectStatus.COMPLETED)

    @property
    def portfolio(self):
        """Return a list of thumbnails (or Project objects) representing the user's portfolio.

        By default this will return the thumbnails for completed projects. If you need full
        Project objects, use `profile.completed_projects`.
        """
        return list(self.completed_projects.values_list('thumbnail', flat=True))

    @property
    def active_projects(self):
        """Return a queryset of this user's active/in-progress projects."""
        return Project.objects.filter(client=self.user, status=Project.ProjectStatus.IN_PROGRESS)

    @property
    def projects_posted(self):
        """Return the number of projects this user has posted (created_projects related_name)."""
        return self.user.created_projects.count()

    @property
    def average_rating(self):
        """Return the aggregated average rating calculated from Review records.

        If the `rating` field on Profile is already populated it will be returned as a
        convenience; otherwise the value is computed from Review.reviewee (reviews_received).
        """
        # Use cached rating if present
        if self.rating is not None:
            return float(self.rating)

        # Aggregate from Review model via the user's related name `reviews_received`
        agg = self.user.reviews_received.aggregate(avg=Avg('rating'))
        avg = agg.get('avg')
        return float(avg) if avg is not None else None

    def __str__(self):
        roles = ', '.join([role.name for role in self.user.roles.all()])
        return f"{self.user.username}'s Profile ({roles})"

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