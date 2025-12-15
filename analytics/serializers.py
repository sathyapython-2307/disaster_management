from rest_framework import serializers
from .models import DisasterAnalytics, AlertAnalytics, UserActivityLog, SystemMetrics

class DisasterAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterAnalytics
        fields = ['id', 'disaster_type', 'date', 'total_events', 'high_risk_events', 'avg_risk_score', 'total_affected_population', 'total_estimated_damage', 'affected_regions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AlertAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertAnalytics
        fields = ['id', 'date', 'total_alerts', 'critical_alerts', 'high_alerts', 'medium_alerts', 'low_alerts', 'avg_response_time_minutes', 'acknowledgment_rate', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserActivityLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'user_name', 'activity_type', 'description', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return None


class SystemMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMetrics
        fields = ['id', 'timestamp', 'api_response_time_ms', 'database_query_time_ms', 'active_users', 'total_events_processed', 'alerts_generated', 'cpu_usage_percent', 'memory_usage_percent']
        read_only_fields = ['id', 'timestamp']
