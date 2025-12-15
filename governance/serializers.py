from rest_framework import serializers
from .models import RolePermission, PolicyConfiguration, ComplianceLog, DataRetentionPolicy

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class PolicyConfigurationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = PolicyConfiguration
        fields = ['id', 'name', 'policy_type', 'rules', 'is_active', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class ComplianceLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ComplianceLog
        fields = ['id', 'user', 'user_name', 'action', 'status', 'details', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return None


class DataRetentionPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRetentionPolicy
        fields = ['id', 'data_type', 'retention_days', 'archive_after_days', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

