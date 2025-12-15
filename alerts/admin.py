from django.contrib import admin
from .models import Alert, AlertDispatch, AlertThreshold, NotificationPreference

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'status', 'created_at', 'acknowledged_by']
    list_filter = ['severity', 'status', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['id', 'created_at', 'sent_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Alert Information', {
            'fields': ('disaster_event', 'title', 'message')
        }),
        ('Status', {
            'fields': ('severity', 'status', 'acknowledged_by', 'acknowledged_at')
        }),
        ('Timeline', {
            'fields': ('created_at', 'sent_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AlertDispatch)
class AlertDispatchAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'channel', 'status', 'sent_at', 'read_at']
    list_filter = ['channel', 'status', 'created_at']
    search_fields = ['recipient__username', 'recipient_address']
    readonly_fields = ['id', 'created_at', 'sent_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Dispatch Information', {
            'fields': ('alert', 'recipient', 'channel', 'recipient_address')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Timeline', {
            'fields': ('created_at', 'sent_at', 'read_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AlertThreshold)
class AlertThresholdAdmin(admin.ModelAdmin):
    list_display = ['disaster_type', 'risk_score_threshold', 'confidence_threshold', 'is_active']
    list_filter = ['disaster_type', 'is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Threshold Configuration', {
            'fields': ('disaster_type', 'risk_score_threshold', 'confidence_threshold', 'is_active')
        }),
        ('Notification Settings', {
            'fields': ('notification_channels', 'recipient_roles')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_enabled', 'sms_enabled', 'push_enabled', 'in_app_enabled']
    list_filter = ['email_enabled', 'sms_enabled', 'push_enabled', 'in_app_enabled']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id', 'updated_at']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Notification Channels', {
            'fields': ('email_enabled', 'sms_enabled', 'push_enabled', 'in_app_enabled')
        }),
        ('Preferences', {
            'fields': ('disaster_types', 'min_risk_score', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Metadata', {
            'fields': ('id', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
