from django.contrib import admin
from .models import Bug

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    """Admin configuration for the Bug model."""
    
    # Fields to display in the list view
    list_display = (
        'bug_id', 
        'subject', 
        'status', 
        'priority', 
        'modified_count', 
        'created_at', 
        'updated_at'
    )
    
    # Fields that can be used for filtering in the right sidebar
    list_filter = ('status', 'priority', 'created_at', 'updated_at')
    
    # Fields that can be searched
    search_fields = ('bug_id', 'subject', 'description')
    
    # Fields that cannot be edited
    readonly_fields = ('bug_id', 'modified_count', 'created_at', 'updated_at')
    
    # Default ordering
    ordering = ('-updated_at',)
    
    # Fields grouped by fieldsets
    fieldsets = (
        ('Bug Information', {
            'fields': ('bug_id', 'subject', 'description')
        }),
        ('Status Information', {
            'fields': ('status', 'priority')
        }),
        ('Modification Information', {
            'fields': ('modified_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Custom actions
    actions = ['mark_as_resolved', 'mark_as_closed']
    
    def mark_as_resolved(self, request, queryset):
        """Mark selected bugs as resolved."""
        updated = queryset.update(status='resolved')
        self.message_user(request, f"{updated} bug(s) successfully marked as resolved.")
    mark_as_resolved.short_description = "Mark selected bugs as resolved"
    
    def mark_as_closed(self, request, queryset):
        """Mark selected bugs as closed."""
        updated = queryset.update(status='closed')
        self.message_user(request, f"{updated} bug(s) successfully marked as closed.")
    mark_as_closed.short_description = "Mark selected bugs as closed"
    
    # Custom display for datetime fields
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")
    get_created_at.short_description = "Created"
    
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M")
    get_updated_at.short_description = "Updated"

# If you have a BugModification model, you can also register it
# Uncomment this code if you have this model
'''
@admin.register(BugModification)
class BugModificationAdmin(admin.ModelAdmin):
    """Admin configuration for the BugModification model."""
    list_display = ('bug', 'field_modified', 'old_value', 'new_value', 'modified_at')
    list_filter = ('field_modified', 'modified_at')
    search_fields = ('bug__bug_id', 'field_modified')
    ordering = ('-modified_at',)
'''