from django.contrib import admin
from .models import Project, InvestmentApplication, UserProfile


class CollaboratorInline(admin.TabularInline):
    model = Project.collaborators.through  
    extra = 1  
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'sector', 'country', 'status', 'formatted_investment_required', 'owner', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('sector', 'country', 'status', 'is_featured')  
    search_fields = ('title', 'sector', 'country', 'owner__username')  
    inlines = [CollaboratorInline]  s

    def formatted_investment_required(self, obj):
        """Format the investment required field for display in the admin list."""
        return obj.formatted_investment_required
    formatted_investment_required.short_description = "Investment Required"

@admin.register(InvestmentApplication)
class InvestmentApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'sector', 'country', 'investment_required', 'contact_information', 'submitted_at')
    list_filter = ('sector', 'country', 'submitted_at')  
    search_fields = ('user__username', 'title', 'sector', 'country')  

# Register the UserProfile model for admin management
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'country')  
    search_fields = ('user__username', 'country')  
