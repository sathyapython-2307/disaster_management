"""
Data sync module for importing uploaded files into disaster events
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from disasters.models import DisasterEvent, DisasterData
from core.models import DataSource, AuditLog
from core.file_reader import FileReaderFactory
import os

logger = logging.getLogger(__name__)


class DataSyncManager:
    """Manages syncing data from uploaded files to disaster models"""
    
    # Field mapping for DisasterEvent
    DISASTER_EVENT_FIELDS = {
        'disaster_type': str,
        'status': str,
        'latitude': float,
        'longitude': float,
        'location_name': str,
        'risk_score': float,
        'confidence_level': float,
        'magnitude': float,
        'wind_speed_kmh': float,
        'rainfall_mm': float,
        'affected_area_sqkm': float,
        'predicted_time': datetime,
        'start_time': datetime,
        'end_time': datetime,
        'estimated_affected_population': int,
        'estimated_damage_usd': int,
    }
    
    @classmethod
    def sync_data_source(cls, data_source: DataSource, user=None) -> Tuple[int, List[str]]:
        """
        Sync a single data source
        
        Returns:
            Tuple of (records_processed, list of errors)
        """
        logger.info(f"Starting sync for data source: {data_source.name} ({data_source.id})")
        
        try:
            # Validate file_path is not empty
            if not data_source.file_path or data_source.file_path.strip() == '':
                raise ValueError(f"DataSource {data_source.name} has no file_path configured")
            
            # Construct full file path
            file_path = os.path.join(settings.MEDIA_ROOT, data_source.file_path)
            
            # Read the file
            records = FileReaderFactory.read_file(file_path)
            logger.info(f"Read {len(records)} records from {data_source.name}")
            
            # Process records based on source type
            if data_source.source_type in ['csv', 'file']:
                records_processed, errors = cls._process_disaster_records(
                    records, data_source
                )
            else:
                # For other source types, just log as generic data
                records_processed = len(records)
                errors = []
            
            # Update last sync time
            data_source.last_sync = timezone.now()
            data_source.save()
            
            # Log the sync action
            if user:
                AuditLog.objects.create(
                    user=user,
                    action='model_change',
                    resource_type='DataSync',
                    resource_id=str(data_source.id),
                    description=f"Synced data source: {data_source.name} ({records_processed} records)",
                    new_values={'records_processed': records_processed, 'errors': len(errors)}
                )
            
            logger.info(f"Sync completed: {records_processed} records, {len(errors)} errors")
            return records_processed, errors
            
        except Exception as e:
            logger.error(f"Error syncing data source {data_source.name}: {str(e)}", exc_info=True)
            return 0, [str(e)]
    
    @classmethod
    def _process_disaster_records(
        cls, records: List[Dict[str, Any]], data_source: DataSource
    ) -> Tuple[int, List[str]]:
        """
        Process records as disaster events
        
        Returns:
            Tuple of (records_processed, list of errors)
        """
        processed = 0
        errors = []
        
        for idx, record in enumerate(records):
            try:
                # Extract and validate required fields
                disaster_data = cls._extract_disaster_data(record)
                
                # Skip if critical fields missing
                if not disaster_data.get('disaster_type') or not disaster_data.get('location_name'):
                    errors.append(f"Row {idx}: Missing disaster_type or location_name")
                    continue
                
                # Check for duplicates (same type, location, and time)
                existing = DisasterEvent.objects.filter(
                    disaster_type=disaster_data['disaster_type'],
                    location_name=disaster_data['location_name'],
                    predicted_time=disaster_data.get('predicted_time', timezone.now())
                ).first()
                
                if existing:
                    # Update existing record
                    for field, value in disaster_data.items():
                        if hasattr(existing, field) and value is not None:
                            setattr(existing, field, value)
                    existing.save()
                    logger.debug(f"Updated existing disaster event: {existing.id}")
                else:
                    # Create new record
                    disaster = DisasterEvent.objects.create(**disaster_data)
                    logger.debug(f"Created new disaster event: {disaster.id}")
                
                # Add data points if available
                if 'data_points' in record:
                    cls._create_data_points(disaster, record['data_points'], data_source)
                
                processed += 1
                
            except ValueError as e:
                errors.append(f"Row {idx}: Validation error - {str(e)}")
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")
                logger.error(f"Error processing record {idx}: {str(e)}")
        
        return processed, errors
    
    # Mapping for string severity/risk values
    SEVERITY_MAPPING = {
        'critical': 90.0,
        'high': 75.0,
        'medium': 50.0,
        'low': 25.0,
        'very high': 95.0,
        'severe': 85.0,
        'moderate': 50.0,
        'minor': 20.0,
    }
    
    @classmethod
    def _extract_disaster_data(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract disaster event data from a record
        Attempts to map common field names
        """
        # Normalize field names (lowercase, replace spaces with underscores)
        normalized = {
            k.lower().replace(' ', '_').replace('-', '_'): v 
            for k, v in record.items()
        }
        
        disaster_data = {}
        
        # Map fields
        field_mappings = {
            'disaster_type': ['disaster_type', 'type', 'event_type', 'disaster'],
            'status': ['status', 'state'],
            'latitude': ['latitude', 'lat', 'y'],
            'longitude': ['longitude', 'lon', 'long', 'x'],
            'location_name': ['location_name', 'location', 'place', 'area'],
            'risk_score': ['risk_score', 'risk', 'severity'],
            'confidence_level': ['confidence_level', 'confidence'],
            'magnitude': ['magnitude', 'mag'],
            'wind_speed_kmh': ['wind_speed_kmh', 'wind_speed', 'windspeed'],
            'rainfall_mm': ['rainfall_mm', 'rainfall', 'rain'],
            'affected_area_sqkm': ['affected_area_sqkm', 'area', 'affected_area'],
            'predicted_time': ['predicted_time', 'time', 'timestamp', 'datetime'],
            'start_time': ['start_time', 'start'],
            'end_time': ['end_time', 'end'],
            'estimated_affected_population': ['estimated_affected_population', 'population', 'people'],
            'estimated_damage_usd': ['estimated_damage_usd', 'damage', 'cost'],
        }
        
        for target_field, source_fields in field_mappings.items():
            for source_field in source_fields:
                if source_field in normalized and normalized[source_field]:
                    try:
                        value = normalized[source_field]
                        
                        # Type conversion
                        if target_field == 'risk_score' or target_field == 'confidence_level':
                            # Try numeric conversion first
                            try:
                                value = float(value)
                            except (ValueError, TypeError):
                                # Try string mapping (High, Critical, etc.)
                                str_val = str(value).strip().lower()
                                if str_val in cls.SEVERITY_MAPPING:
                                    value = cls.SEVERITY_MAPPING[str_val]
                                else:
                                    raise ValueError(f"Cannot convert '{value}' to numeric risk score")
                        elif target_field in ['latitude', 'longitude', 'magnitude', 'wind_speed_kmh', 
                                           'rainfall_mm', 'affected_area_sqkm']:
                            value = float(value)
                        elif target_field in ['estimated_affected_population', 'estimated_damage_usd']:
                            value = int(float(value))
                        elif target_field in ['predicted_time', 'start_time', 'end_time']:
                            value = cls._parse_datetime(value)
                        else:
                            value = str(value).lower() if target_field == 'disaster_type' else str(value)
                        
                        disaster_data[target_field] = value
                        break
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Could not convert {source_field}={value} to {target_field}: {e}")
                        continue
        
        # Set required defaults if missing
        if 'status' not in disaster_data:
            disaster_data['status'] = 'predicted'
        if 'predicted_time' not in disaster_data:
            disaster_data['predicted_time'] = timezone.now()
        if 'risk_score' not in disaster_data:
            disaster_data['risk_score'] = 50.0
        if 'confidence_level' not in disaster_data:
            disaster_data['confidence_level'] = 50.0
        
        return disaster_data
    
    @classmethod
    def _parse_datetime(cls, value: Any) -> datetime:
        """Parse datetime from various formats"""
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            # Try common formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(value.strip(), fmt)
                    # Make it timezone-aware
                    if dt.tzinfo is None:
                        dt = timezone.make_aware(dt)
                    return dt
                except ValueError:
                    continue
            
            raise ValueError(f"Could not parse datetime: {value}")
        
        raise ValueError(f"Invalid datetime type: {type(value)}")
    
    @classmethod
    def _create_data_points(
        cls, event: DisasterEvent, data_points: Dict[str, Any], data_source: DataSource
    ) -> None:
        """Create DisasterData points for an event"""
        if isinstance(data_points, dict):
            data_points = [data_points]
        
        for point in data_points:
            try:
                DisasterData.objects.create(
                    event=event,
                    data_type=point.get('data_type', 'measurement'),
                    value=float(point.get('value', 0)),
                    unit=point.get('unit', ''),
                    source=data_source.name,
                    timestamp=cls._parse_datetime(point.get('timestamp', timezone.now()))
                )
            except Exception as e:
                logger.warning(f"Could not create data point: {e}")
    
    @classmethod
    def sync_all_active_sources(cls, user=None) -> Dict[str, Any]:
        """
        Sync all active data sources based on their sync interval
        
        Returns:
            Dictionary with sync results
        """
        active_sources = DataSource.objects.filter(is_active=True)
        results = {
            'total_sources': active_sources.count(),
            'synced': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
        
        now = timezone.now()
        
        for source in active_sources:
            try:
                # Check if sync is needed based on interval
                if source.last_sync:
                    next_sync = source.last_sync + timedelta(minutes=source.sync_interval_minutes)
                    if now < next_sync:
                        results['skipped'] += 1
                        results['details'].append({
                            'source': source.name,
                            'status': 'skipped',
                            'reason': 'Not due for sync'
                        })
                        continue
                
                # Sync the source
                processed, errors = cls.sync_data_source(source, user)
                
                if errors:
                    results['failed'] += 1
                    results['details'].append({
                        'source': source.name,
                        'status': 'failed',
                        'processed': processed,
                        'errors': errors
                    })
                else:
                    results['synced'] += 1
                    results['details'].append({
                        'source': source.name,
                        'status': 'success',
                        'processed': processed
                    })
                
            except Exception as e:
                logger.error(f"Error syncing source {source.name}: {e}", exc_info=True)
                results['failed'] += 1
                results['details'].append({
                    'source': source.name,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
