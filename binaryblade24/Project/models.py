from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    def __str__(self) -> str:
        return self.name
    
    
class Project(models.Model):

    title = models.CharField(unique=True, blank=False, max_length=100)
    description = models.CharField(blank=False, max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    project_id = models.IntegerField(unique=True, max_length=20, blank=False)
    client_id = models.IntegerField(unique=True, max_length=20, blank=False)
    project_id = models.IntegerField(unique=True, max_length=20, blank=False)
    status = models.CharField(max_length=20)
    Created_at = models.DateTimeField(auto_now = True)
    
    # Foreign Key to link a product to a category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)