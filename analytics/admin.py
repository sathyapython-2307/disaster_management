from django.contrib import admin
from .models import DisasterAnalytics, AlertAnalytics, UserActivityLog, SystemMetrics

@admin.register(DisasterAnalytics)
class DisasterAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['disaster_type', 'date', 'total_events', 'high_risk_events', 'avg_risk_score']
    list_filter = ['disaster_type', 'date']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    fieldsets = (
        ('Analytics Information', {
            'fields': ('disaster_type', 'date')
        }),
        ('Statistics', {
            'fields': ('total_events', 'high_risk_events', 'avg_risk_score')
        }),
        ('Impact', {
            'fields': ('total_affected_population', 'total_estimated_damage')
        }),
        ('Geographic Data', {
            'fields': ('affected_regions',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AlertAnalytics)
class AlertAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_alerts', 'critical_alerts', 'high_alerts', 'avg_response_time_minutes']
    list_filter = ['date']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Alert Statistics', {
            'fields': ('total_alerts', 'critical_alerts', 'high_alerts', 'medium_alerts', 'low_alerts')
        }),
        ('Performance', {
            'fields': ('avg_response_time_minutes', 'acknowledgment_rate')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp']
    list_filter = ['activity_type', 'timestamp', 'user']
    search_fields = ['user__username', 'activity_type', 'description']
    readonly_fields = ['id', 'timestamp', 'user', 'activity_type', 'description']
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'activity_type', 'description')
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

@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'cpu_usage_percent', 'memory_usage_percent', 'active_users', 'api_response_time_ms']
    list_filter = ['timestamp']
    readonly_fields = ['id', 'timestamp', 'api_response_time_ms', 'database_query_time_ms', 'active_users', 'total_events_processed', 'alerts_generated', 'cpu_usage_percent', 'memory_usage_percent']
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Performance Metrics', {
            'fields': ('api_response_time_ms', 'database_query_time_ms')
        }),
        ('Activity Metrics', {
            'fields': ('active_users', 'total_events_processed', 'alerts_generated')
        }),
        ('System Health', {
            'fields': ('cpu_usage_percent', 'memory_usage_percent')
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
