from django.conf import settings
from django.db import models

# Create your models here.
class Category(models.Model):
    """
    Hierarchical category system for projects/gigs with 3 levels.
    
    Supports three levels:
    - **Level 1** Main categories (parent=None): e.g., "Core Development"
    - **Level 2** Subcategories (parent=Category): e.g., "Frontend Development"
    - **Level 3** Items (stored in items JSON): e.g., ["SPA Development", "Responsive Design"]
    
    Examples:
        Core Development (Level 1)
          ├── Frontend Development (Level 2)
          │     ├── SPA Development (React, Vue, Angular) (Level 3)
          │     ├── Responsive Web Design (HTML/CSS/JS) (Level 3)
          │     └── UI/UX Implementation (Level 3)
          └── Backend Development (Level 2)
                ├── API Development (REST/GraphQL) (Level 3)
                └── Database Modeling & Mgmt (Level 3)
    """
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text="Leave empty for main categories, select a parent for subcategories"
    )
    description = models.TextField(blank=True, help_text="Brief description of this category")
    
    # Level 3: Items/Tasks - stored as JSON array for flexibility
    items = models.JSONField(
        default=list,
        blank=True,
        help_text="List of specific items/tasks for this category (only for Level 2 subcategories)"
    )
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def is_main_category(self):
        """Returns True if this is a top-level category (Level 1)"""
        return self.parent is None
    
    def is_subcategory(self):
        """Returns True if this is a subcategory (Level 2)"""
        return self.parent is not None
    
    
class Project(models.Model):

    title = models.CharField(unique=True, blank=False, max_length=200)
    description = models.CharField(blank=False, max_length=2500)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
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
    
    # Project type for hybrid marketplace (Fiverr + Upwork model)
    class ProjectType(models.TextChoices):
        GIG = 'GIG', 'Gig'      # Freelancer-created service offering (Fiverr-style)
        JOB = 'JOB', 'Job'      # Client-created work requirement (Upwork-style)

        
    # client id will be created automatically
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='created_projects')

    # Setting status: use the choices defined in ProjectStatus
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.OPEN,
        help_text="The current status of this project",
    )
    
    # Project type: GIG (freelancer service) or JOB (client requirement)
    project_type = models.CharField(
        max_length=10,
        choices=ProjectType.choices,
        default=ProjectType.JOB,
        help_text="Type of project: GIG (freelancer offers service) or JOB (client needs work done)"
    )

    def __str__(self):
        return self.title
    
    def is_gig(self):
        """Returns True if this is a freelancer-created service offering"""
        return self.project_type == self.ProjectType.GIG
    
    def is_job(self):
        """Returns True if this is a client-created job posting"""
        return self.project_type == self.ProjectType.JOB