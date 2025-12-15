from django.contrib import admin
from .models import DisasterEvent, DisasterData, RiskModel, HistoricalDisaster

@admin.register(DisasterEvent)
class DisasterEventAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'disaster_type', 'status', 'risk_score', 'predicted_time']
    list_filter = ['disaster_type', 'status', 'predicted_time']
    search_fields = ['location_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'predicted_time'
    fieldsets = (
        ('Event Information', {
            'fields': ('disaster_type', 'status', 'location_name', 'latitude', 'longitude')
        }),
        ('Risk Assessment', {
            'fields': ('risk_score', 'confidence_level')
        }),
        ('Event Details', {
            'fields': ('magnitude', 'wind_speed_kmh', 'rainfall_mm', 'affected_area_sqkm')
        }),
        ('Impact', {
            'fields': ('estimated_affected_population', 'estimated_damage_usd')
        }),
        ('Timeline', {
            'fields': ('predicted_time', 'start_time', 'end_time')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DisasterData)
class DisasterDataAdmin(admin.ModelAdmin):
    list_display = ['event', 'data_type', 'value', 'unit', 'timestamp']
    list_filter = ['data_type', 'source', 'timestamp']
    search_fields = ['event__location_name', 'data_type']
    readonly_fields = ['id']
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Data Information', {
            'fields': ('event', 'data_type', 'value', 'unit', 'source', 'timestamp')
        }),
        ('Metadata', {
            'fields': ('metadata', 'id'),
            'classes': ('collapse',)
        }),
    )

@admin.register(RiskModel)
class RiskModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'disaster_type', 'version', 'is_active', 'accuracy_score']
    list_filter = ['disaster_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Model Information', {
            'fields': ('name', 'disaster_type', 'version', 'description')
        }),
        ('Configuration', {
            'fields': ('parameters', 'weights', 'thresholds')
        }),
        ('Performance', {
            'fields': ('accuracy_score', 'is_active')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(HistoricalDisaster)
class HistoricalDisasterAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'disaster_type', 'occurrence_date', 'casualties', 'damage_usd']
    list_filter = ['disaster_type', 'occurrence_date']
    search_fields = ['location_name', 'description']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'occurrence_date'
    fieldsets = (
        ('Disaster Information', {
            'fields': ('disaster_type', 'location_name', 'occurrence_date')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Impact', {
            'fields': ('magnitude', 'casualties', 'damage_usd')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
