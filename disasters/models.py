from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class DisasterEvent(models.Model):
    DISASTER_TYPES = (
        ('flood', 'Flood'),
        ('earthquake', 'Earthquake'),
        ('cyclone', 'Cyclone'),
        ('wildfire', 'Wildfire'),
    )
    
    STATUS_CHOICES = (
        ('predicted', 'Predicted'),
        ('active', 'Active'),
        ('contained', 'Contained'),
        ('resolved', 'Resolved'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disaster_type = models.CharField(max_length=50, choices=DISASTER_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='predicted')
    latitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    location_name = models.CharField(max_length=255)
    
    # Risk scoring
    risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    confidence_level = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Event details
    magnitude = models.FloatField(null=True, blank=True)  # For earthquakes
    wind_speed_kmh = models.FloatField(null=True, blank=True)  # For cyclones
    rainfall_mm = models.FloatField(null=True, blank=True)  # For floods
    affected_area_sqkm = models.FloatField(null=True, blank=True)
    
    # Timestamps
    predicted_time = models.DateTimeField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Impact estimation
    estimated_affected_population = models.IntegerField(default=0)
    estimated_damage_usd = models.BigIntegerField(default=0)
    
    class Meta:
        ordering = ['-predicted_time']
        indexes = [
            models.Index(fields=['disaster_type', 'status']),
            models.Index(fields=['risk_score']),
            models.Index(fields=['predicted_time']),
        ]
    
    def __str__(self):
        return f"{self.get_disaster_type_display()} - {self.location_name}"


class DisasterData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(DisasterEvent, on_delete=models.CASCADE, related_name='data_points')
    data_type = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    source = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    metadata = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.data_type} - {self.value} {self.unit}"


class RiskModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    disaster_type = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    # Model parameters
    parameters = models.JSONField()
    weights = models.JSONField()
    thresholds = models.JSONField()
    
    is_active = models.BooleanField(default=False)
    accuracy_score = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class HistoricalDisaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disaster_type = models.CharField(max_length=50)
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    occurrence_date = models.DateField()
    magnitude = models.FloatField(null=True, blank=True)
    casualties = models.IntegerField(default=0)
    damage_usd = models.BigIntegerField(default=0)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-occurrence_date']
        verbose_name_plural = "Historical Disasters"
    
    def __str__(self):
        return f"{self.disaster_type} - {self.location_name} ({self.occurrence_date})"
