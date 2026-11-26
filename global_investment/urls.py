from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.i18n import set_language
from projects import views  
from projects.views import landing_page, about_page, create_project, my_projects
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from projects.sitemaps import StaticViewSitemap, ProjectSitemap
from projects.views import apply_to_invest




sitemaps = {
    "static": StaticViewSitemap(),
    "projects": ProjectSitemap(),
}

# Language Switcher
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  
    path('i18n/setlang/', set_language, name='set_language'),
]

# Apply `i18n_patterns` to make URLs translation-aware
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),  
    path('', landing_page, name='landing'),  
    path('about/', about_page, name='about'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('projects/mine/', my_projects, name='my_projects'),  
    path('', include('projects.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),  
    path('users/', include('users.urls')),  
    path('apply-to-invest/<int:project_id>/', views.apply_to_invest, name='apply_to_invest'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
  
)

# Serve static/media files (during development)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
