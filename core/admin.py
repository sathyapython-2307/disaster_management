from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, AuditLog, SystemConfiguration, Geofence, DataSource

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('role', 'organization', 'phone', 'is_active_user', 'last_login_ip')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role Assignment', {'fields': ('role', 'organization', 'phone')}),
    )
    list_display = ['username', 'email', 'role', 'is_active_user', 'created_at']
    list_filter = ['role', 'is_active_user', 'created_at']
    search_fields = ['username', 'email', 'organization']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make role field required
        if 'role' in form.base_fields:
            form.base_fields['role'].required = True
        return form

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'resource_type', 'description']
    list_filter = ['action', 'resource_type', 'timestamp']
    search_fields = ['user__username', 'description', 'resource_id']
    readonly_fields = ['timestamp', 'id', 'user', 'action', 'resource_type', 'resource_id', 'description', 'old_values', 'new_values', 'ip_address']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'updated_by', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['key', 'description']
    readonly_fields = ['id', 'updated_at']
    fieldsets = (
        ('Configuration', {
            'fields': ('key', 'value', 'description')
        }),
        ('Metadata', {
            'fields': ('updated_by', 'updated_at', 'id'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Geofence)
class GeofenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']
    fieldsets = (
        ('Geofence Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Location', {
            'fields': ('coordinates', 'radius_km')
        }),
        ('Configuration', {
            'fields': ('disaster_types',)
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

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'is_active', 'last_sync', 'created_by']
    list_filter = ['source_type', 'is_active', 'created_at']
    search_fields = ['name', 'endpoint']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_sync', 'created_by']
    fieldsets = (
        ('Data Source Information', {
            'fields': ('name', 'source_type', 'is_active')
        }),
        ('Connection Details', {
            'fields': ('endpoint', 'api_key')
        }),
        ('Synchronization', {
            'fields': ('sync_interval_minutes', 'last_sync')
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
