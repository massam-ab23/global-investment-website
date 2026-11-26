from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from .views import apply_to_invest
from django.views.i18n import set_language
from .views import paypal_payment_success
from . import views
from django.contrib.sitemaps.views import sitemap
from projects.sitemaps import StaticViewSitemap, ProjectSitemap
from .views import sector_detail
from django.conf import settings  
from django.conf.urls.static import static  
from .views import search_results
from .views import calendar_view  
from .views import news_view  
from .views import multisector_view  
from .views import history_view, music_view  
from .views import paypal_webhook

from .views import (
    project_detail,
    edit_project,
    delete_project,
    remove_collaborator,
    my_projects,
    notifications_view,
    mark_notifications_as_read,
    create_project,
    investment_success,
    delete_notification,
    landing_page,
    profile,
    edit_profile,
    contact_us,

       
)

sitemaps = {
    "static": StaticViewSitemap(),
    "projects": ProjectSitemap(),
}


urlpatterns = [
    path('project/<int:pk>/', project_detail, name='project_detail'),  
    path('project/edit/<int:pk>/', edit_project, name='edit_project'),  
    path('project/delete/<int:pk>/', delete_project, name='delete_project'),  
    path('project/<int:project_id>/remove-collaborator/<int:collaborator_id>/', remove_collaborator, name='remove_collaborator'),  
    path('my-projects/', my_projects, name='my_projects'),  
    path('notifications/', notifications_view, name='notifications'),  
    path('notifications/mark-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),  

    path('project/create/', create_project, name='create_project'),  
    path('apply-to-invest/success/', investment_success, name='investment_success'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
   
    path('apply-to-invest/<int:project_id>/', apply_to_invest, name='apply_to_invest'),
    path('', landing_page, name='landing'),  
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('edit-user-profile/<int:user_id>/', edit_profile, name='edit_user_profile'),  
    path('contact-us/', views.contact_us, name='contact_us'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language-selection/', views.language_selection, name='language_selection'),
    path('i18n/setlang/', set_language, name='set_language'),  
    path("paypal-success/", paypal_payment_success, name="paypal_success"), 
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"), 
    path("sector/<str:sector_name>/", sector_detail, name="sector_detail"),
    path("apply/<str:sector_name>/", apply_to_invest, name="apply_to_invest"),
    path('search/', search_results, name='search_results'),
    path('calendar/', calendar_view, name='calendar'),
    path('news/', news_view, name='news'),
    path('multisector/', multisector_view, name='multisector'),  
    path("history/", history_view, name="history"),  
    path("music/", music_view, name="music"),        
    path("paypal-webhook/", paypal_webhook, name="paypal_webhook"),
    



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

