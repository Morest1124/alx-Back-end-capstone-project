"""
SEO Sitemaps for BinaryBlade24 Freelancing Platform

This module defines sitemaps for different sections of the site to help
search engines discover and index content efficiently.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Project.models import Project, Category


class ProjectSitemap(Sitemap):
    """
    Sitemap for all open projects/gigs.
    High priority since these are the main content pages users search for.
    """
    changefreq = "daily"
    priority = 0.8
    
    def items(self):
        """Return all open projects that should be indexed."""
        return Project.objects.filter(status=Project.ProjectStatus.OPEN)
    
    def lastmod(self, obj):
        """Return the last modification date of the project."""
        return obj.updated_at
    
    def location(self, obj):
        """Return the URL for the project detail page."""
        # Adjust this based on your frontend routing
        # For now using a simple /projects/{id} pattern
        return f'/projects/{obj.id}/'


class CategorySitemap(Sitemap):
    """
    Sitemap for project categories.
    Helps users discover projects by category.
    """
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        """Return all categories."""
        return Category.objects.all()
    
    def location(self, obj):
        """Return the URL for the category page using slug."""
        return f'/category/{obj.slug}/'


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages like home, about, contact, etc.
    """
    priority = 0.5
    changefreq = "monthly"
    
    def items(self):
        """Return list of static page names."""
        # Add more static pages as you create them
        return ['api-home']
    
    def location(self, item):
        """Return the URL for static pages."""
        return reverse(item)
