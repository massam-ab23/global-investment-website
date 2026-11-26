from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project

class StaticViewSitemap(Sitemap):
    """Handles static pages in the sitemap."""
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            "landing", "about", "create_project", "contact_us"
        ]  

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    """Handles dynamically generated project pages."""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse("project_detail", args=[obj.id])  
