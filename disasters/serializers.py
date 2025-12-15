from rest_framework import serializers
from .models import DisasterEvent, DisasterData, RiskModel, HistoricalDisaster

class DisasterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterEvent
        fields = ['id', 'disaster_type', 'status', 'latitude', 'longitude', 'location_name', 'risk_score', 'confidence_level', 'magnitude', 'wind_speed_kmh', 'rainfall_mm', 'affected_area_sqkm', 'predicted_time', 'start_time', 'end_time', 'estimated_affected_population', 'estimated_damage_usd', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DisasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterData
        fields = ['id', 'event', 'data_type', 'value', 'unit', 'source', 'timestamp', 'metadata']
        read_only_fields = ['id']


class RiskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskModel
        fields = ['id', 'name', 'disaster_type', 'version', 'description', 'parameters', 'weights', 'thresholds', 'is_active', 'accuracy_score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class HistoricalDisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalDisaster
        fields = ['id', 'disaster_type', 'location_name', 'latitude', 'longitude', 'occurrence_date', 'magnitude', 'casualties', 'damage_usd', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
