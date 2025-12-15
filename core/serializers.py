from rest_framework import serializers
from .models import CustomUser, AuditLog, Geofence, DataSource

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'organization', 'phone', 'is_active_user', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_name', 'action', 'resource_type', 'resource_id', 'description', 'old_values', 'new_values', 'ip_address', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return None


class GeofenceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Geofence
        fields = ['id', 'name', 'description', 'coordinates', 'radius_km', 'disaster_types', 'is_active', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class DataSourceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'source_type', 'endpoint', 'file_path', 'is_active', 'last_sync', 'sync_interval_minutes', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_sync', 'created_by']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None
    def validate(self, data):
        source_type = data.get('source_type')
        endpoint = data.get('endpoint')
        file_path = data.get('file_path')
        
        # Validate that appropriate field is provided based on source type
        if source_type in ['file', 'csv']:
            if not file_path:
                raise serializers.ValidationError("File path is required for file-based sources")
        elif source_type in ['api', 'database', 'weather', 'stream']:
            if not endpoint:
                raise serializers.ValidationError("Endpoint/URL is required for this source type")
        
        return data
