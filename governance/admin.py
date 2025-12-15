from django.contrib import admin
from .models import RolePermission, PolicyConfiguration, ComplianceLog, DataRetentionPolicy

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['role', 'permission', 'description']
    readonly_fields = ['id', 'created_at']
    fieldsets = (
        ('Permission Information', {
            'fields': ('role', 'permission', 'description')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PolicyConfiguration)
class PolicyConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'policy_type', 'is_active', 'created_by', 'created_at']
    list_filter = ['policy_type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Policy Information', {
            'fields': ('name', 'policy_type', 'is_active')
        }),
        ('Configuration', {
            'fields': ('rules',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'id'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ComplianceLog)
class ComplianceLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'status', 'timestamp']
    list_filter = ['status', 'timestamp', 'user']
    search_fields = ['user__username', 'action']
    readonly_fields = ['id', 'timestamp', 'user', 'action', 'status', 'details']
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Compliance Information', {
            'fields': ('user', 'action', 'status')
        }),
        ('Details', {
            'fields': ('details',)
        }),
        ('Metadata', {
            'fields': ('id', 'timestamp'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(DataRetentionPolicy)
class DataRetentionPolicyAdmin(admin.ModelAdmin):
    list_display = ['data_type', 'retention_days', 'archive_after_days', 'is_active']
    list_filter = ['data_type', 'is_active', 'created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Policy Information', {
            'fields': ('data_type', 'is_active')
        }),
        ('Retention Settings', {
            'fields': ('retention_days', 'archive_after_days')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
