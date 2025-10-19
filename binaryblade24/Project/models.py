from django.conf import settings
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    def __str__(self) -> str:
        return self.name
    
    
class Project(models.Model):

    title = models.CharField(unique=True, blank=False, max_length=200)
    description = models.CharField(blank=False, max_length=2500)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    project_id = models.IntegerField(unique=True, blank=False)
    thumbnail = models.ImageField(upload_to='thumbnail/', null=True, blank=True)
    delivery_days = models.DateTimeField(
        null=True, 
        blank=True,
        # verbose_name="Estimated Delivery Date",
        # help_text="The expected date and time the order will be delivered to the customer."
    )
    #Timeline
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
    # Foreign Key to link a product to a category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    #Project status
    class ProjectStatus(models.TextChoices):
        OPEN = 'OPEN' , 'OPEN'
        IN_PROGRESS = 'IN_PROGRESS', 'IN PROGRESS'
        COMPLETED = 'COMPLETED', 'COMPLETED'
        CANCELED = 'CANCELED', 'CANCELED'

        
    # client id will be created automatically
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='created_projects')

    # Setting status: use the choices defined in ProjectStatus
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.OPEN,
        help_text="The current status of this project",
    )