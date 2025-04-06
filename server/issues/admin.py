from django.contrib import admin
from .models import Bug

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    """Admin configuration for the Bug model."""
    
    # Fields to display in the list view
    list_display = ('bug_id', 'subject', 'status', 'priority', 'modified_count', 'created_at', 'updated_at')
    
    # Fields that can be used for filtering in the right sidebar
    list_filter = ('status', 'priority', 'created_at', 'updated_at')
    
    # Fields that can be searched
    search_fields = ('bug_id', 'subject', 'description')
    
    # Fields that cannot be edited
    readonly_fields = ('modified_count', 'created_at', 'updated_at')
    
    # Default ordering
    ordering = ('-updated_at',)