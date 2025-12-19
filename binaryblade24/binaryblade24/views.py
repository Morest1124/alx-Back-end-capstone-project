"""
SEO Views for BinaryBlade24

Provides SEO-related views including robots.txt generation.
"""

from django.http import HttpResponse
from django.conf import settings


def robots_txt(request):
    """
    Generate robots.txt file dynamically.
    
    This tells search engines which pages to crawl and which to avoid.
    Also includes the sitemap URL for easy discovery.
    """
    # Get the current site's domain
    domain = request.get_host()
    protocol = 'https' if request.is_secure() else 'http'
    sitemap_url = f"{protocol}://{domain}/sitemap.xml"
    
    # Define robots.txt content
    lines = [
        "User-agent: *",
        "",
        "# Disallow admin and private API endpoints",
        "Disallow: /admin/",
        "Disallow: /api/auth/",
        "Disallow: /api/dashboard/",
        "Disallow: /api/messages/",
        "Disallow: /api/api-key/",
        "",
        "# Disallow user-uploaded files (except public profiles)",
        "Disallow: /media/uploads/",
        "",
        "# Allow public API endpoints",
        "Allow: /api/projects/",
        "Allow: /api/reviews/",
        "Allow: /api/proposals/",
        "",
        "# Allow everything else",
        "Allow: /",
        "",
        f"# Sitemap location",
        f"Sitemap: {sitemap_url}",
    ]
    
    content = "\n".join(lines)
    return HttpResponse(content, content_type="text/plain")
