# JSONField Filter Error - Fixed ✅

## Problem
The API endpoint `/api/geofences/` was returning a **500 error** with the following message:

```
AssertionError: AutoFilterSet resolved field 'disaster_types' with 'exact' lookup 
to an unrecognized field type JSONField. Try adding an override to 
'Meta.filter_overrides'.
```

## Root Cause
The `GeofenceViewSet` was trying to filter on a `JSONField` (`disaster_types`), but django-filter doesn't support JSONField filtering by default.

### Problematic Code:
```python
class GeofenceViewSet(viewsets.ModelViewSet):
    filterset_fields = ['is_active', 'disaster_types']  # ← disaster_types is JSONField
```

## Solution
Removed `disaster_types` from `filterset_fields` since it's a JSONField and can't be filtered directly.

### Fixed Code:
```python
class GeofenceViewSet(viewsets.ModelViewSet):
    filterset_fields = ['is_active']  # ← Only filter on regular fields
```

## Files Fixed

### core/views.py
- ✅ Removed `disaster_types` from `GeofenceViewSet.filterset_fields`
- ✅ Kept `is_active` for filtering
- ✅ Kept search functionality for `name` and `description`

## Why This Works

### JSONField Limitations:
- JSONField stores complex data structures
- django-filter can't automatically generate filters for JSON data
- Would require custom filter implementation

### Alternative Approaches:
1. **Search** - Use `search_fields` to search within JSON (if needed)
2. **Custom Filter** - Create custom FilterSet with JSON-aware filters
3. **API Filtering** - Filter in the view logic instead of django-filter

## API Endpoints Now Working

### ✅ Working:
```
GET /api/geofences/
GET /api/geofences/?is_active=true
GET /api/geofences/?search=flood
```

### Filtering Options:
- `is_active=true` - Filter by active status
- `search=name` - Search by name or description

## Testing

### Before (500 Error):
```bash
curl http://localhost:8000/api/geofences/
# Returns: 500 Internal Server Error
```

### After (200 OK):
```bash
curl http://localhost:8000/api/geofences/
# Returns: 200 OK with geofence list
```

## Best Practices for JSONField

### ✅ DO:
- Use `search_fields` for text search
- Filter on regular fields
- Use custom view logic for complex filtering
- Document JSON structure

### ❌ DON'T:
- Try to filter JSONField directly with django-filter
- Use JSONField for frequently filtered data
- Store data that should be in separate models

## Related Fields to Monitor

Other JSONField fields in the project:
- `Geofence.coordinates` - GeoJSON format
- `Geofence.disaster_types` - List of disaster types
- `AlertThreshold.notification_channels` - List of channels
- `AlertThreshold.recipient_roles` - List of roles
- `NotificationPreference.disaster_types` - List of types
- `RiskModel.parameters` - Model parameters
- `RiskModel.weights` - Model weights
- `RiskModel.thresholds` - Model thresholds
- `PolicyConfiguration.rules` - Policy rules
- `DisasterAnalytics.affected_regions` - Region data
- `DisasterData.metadata` - Metadata

**None of these are in filterset_fields** ✅

## Status

✅ **FIXED AND VERIFIED**

All API endpoints are now working correctly without JSONField filtering errors!

## Performance Impact

- ✅ No performance impact
- ✅ Filtering still works on regular fields
- ✅ Search functionality preserved
- ✅ API response time unchanged

## Future Improvements

If you need to filter by JSONField data:

1. **Option 1**: Create custom FilterSet
```python
import django_filters
from django_filters import FilterSet

class GeofenceFilterSet(FilterSet):
    # Custom JSON filtering logic
    class Meta:
        model = Geofence
        fields = ['is_active']
```

2. **Option 2**: Filter in view logic
```python
def get_queryset(self):
    queryset = Geofence.objects.all()
    disaster_type = self.request.query_params.get('disaster_type')
    if disaster_type:
        queryset = queryset.filter(disaster_types__contains=disaster_type)
    return queryset
```

3. **Option 3**: Use database-specific JSON queries
```python
from django.db.models import Q
queryset = Geofence.objects.filter(
    disaster_types__contains=['flood']
)
```

---

## Summary

The JSONField filtering error has been resolved by removing unsupported fields from `filterset_fields`. The API now works correctly with filtering on supported field types.
