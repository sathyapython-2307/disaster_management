from rest_framework import serializers
from .models import Alert, AlertDispatch, AlertThreshold, NotificationPreference

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'disaster_event', 'severity', 'status', 'title', 'message', 'created_at', 'sent_at', 'acknowledged_at', 'acknowledged_by']
        read_only_fields = ['id', 'created_at', 'sent_at']


class AlertDispatchSerializer(serializers.ModelSerializer):
    recipient_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = AlertDispatch
        fields = ['id', 'alert', 'recipient', 'recipient_name', 'channel', 'status', 'recipient_address', 'sent_at', 'read_at', 'error_message', 'created_at']
        read_only_fields = ['id', 'created_at', 'sent_at']
    
    def get_recipient_name(self, obj):
        if obj.recipient:
            return obj.recipient.get_full_name()
        return None


class AlertThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertThreshold
        fields = ['id', 'disaster_type', 'risk_score_threshold', 'confidence_threshold', 'notification_channels', 'recipient_roles', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['id', 'user', 'email_enabled', 'sms_enabled', 'push_enabled', 'in_app_enabled', 'disaster_types', 'min_risk_score', 'quiet_hours_start', 'quiet_hours_end', 'updated_at']
        read_only_fields = ['id', 'updated_at']
