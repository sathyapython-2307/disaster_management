from django.db import models
import uuid

class DisasterAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disaster_type = models.CharField(max_length=50)
    
    # Time period
    date = models.DateField()
    
    # Statistics
    total_events = models.IntegerField(default=0)
    high_risk_events = models.IntegerField(default=0)
    avg_risk_score = models.FloatField(default=0)
    
    total_affected_population = models.IntegerField(default=0)
    total_estimated_damage = models.BigIntegerField(default=0)
    
    # Geographic data
    affected_regions = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ('disaster_type', 'date')
        indexes = [
            models.Index(fields=['disaster_type', 'date']),
        ]
    
    def __str__(self):
        return f"{self.disaster_type} - {self.date}"


class AlertAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    
    total_alerts = models.IntegerField(default=0)
    critical_alerts = models.IntegerField(default=0)
    high_alerts = models.IntegerField(default=0)
    medium_alerts = models.IntegerField(default=0)
    low_alerts = models.IntegerField(default=0)
    
    avg_response_time_minutes = models.FloatField(default=0)
    acknowledgment_rate = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ('date',)
    
    def __str__(self):
        return f"Alert Analytics - {self.date}"


class UserActivityLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='activity_logs')
    
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.activity_type}"


class SystemMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Performance metrics
    api_response_time_ms = models.FloatField(default=0)
    database_query_time_ms = models.FloatField(default=0)
    active_users = models.IntegerField(default=0)
    
    # Data metrics
    total_events_processed = models.IntegerField(default=0)
    alerts_generated = models.IntegerField(default=0)
    
    # System health
    cpu_usage_percent = models.FloatField(default=0)
    memory_usage_percent = models.FloatField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Metrics - {self.timestamp}"
