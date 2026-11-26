from django.contrib import admin
from .models import Project, InvestmentApplication, UserProfile


class CollaboratorInline(admin.TabularInline):
    model = Project.collaborators.through  # Use the through table for the ManyToManyField
    extra = 1  # Number of blank collaborator fields to show

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'sector', 'country', 'status', 'formatted_investment_required', 'owner', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('sector', 'country', 'status', 'is_featured')  # Add filters
    search_fields = ('title', 'sector', 'country', 'owner__username')  # Add search fields
    inlines = [CollaboratorInline]  # Inline editing for collaborators

    def formatted_investment_required(self, obj):
        """Format the investment required field for display in the admin list."""
        return obj.formatted_investment_required
    formatted_investment_required.short_description = "Investment Required"

@admin.register(InvestmentApplication)
class InvestmentApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'sector', 'country', 'investment_required', 'contact_information', 'submitted_at')
    list_filter = ('sector', 'country', 'submitted_at')  # Add filters for admin panel
    search_fields = ('user__username', 'title', 'sector', 'country')  # Add search fields

# Register the UserProfile model for admin management
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'country')  # Customize columns to display in the admin
    search_fields = ('user__username', 'country')  # Add search functionality