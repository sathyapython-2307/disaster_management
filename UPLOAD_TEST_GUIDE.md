# 🧪 TESTING CSV UPLOAD FUNCTIONALITY

## Quick Test Steps

### **Step 1: Start Django Server**
```bash
python manage.py runserver
# Server runs on http://127.0.0.1:8000/
```

### **Step 2: Login to Admin Dashboard**
- Go to: `http://127.0.0.1:8000/admin/`
- Username: (your admin username)
- Password: (your admin password)

### **Step 3: Find Upload Option**

**Option A: Via Data Sources Admin**
1. Click "Data Sources" in admin menu
2. Click "Add Data Source" button
3. Look for file upload field
4. Upload your CSV file

**Option B: Via API (Recommended for Testing)**
```bash
# Use the upload endpoint directly
POST /api/data-sources/upload/

# With curl:
curl -X POST http://127.0.0.1:8000/api/data-sources/upload/ \
  -F "file=@upload_test.csv" \
  -F "source_type=csv" \
  -H "X-CSRFToken: <YOUR_CSRF_TOKEN>"
```

---

## CSV File Format

Your CSV should have these columns:

```
event_id, disaster_type, region, state, latitude, longitude, severity, risk_score, affected_population, source, timestamp
```

### Column Descriptions:
- **event_id** - Unique identifier (E001, E002, etc.)
- **disaster_type** - Type: flood, earthquake, cyclone, wildfire, etc.
- **region** - City/Region name
- **state** - State/Province
- **latitude** - Decimal degrees (-90 to 90)
- **longitude** - Decimal degrees (-180 to 180)
- **severity** - Text: Low, Medium, High, Very High
- **risk_score** - Number: 0-100
- **affected_population** - Number of people affected
- **source** - Data source (IMD, USGS, etc.)
- **timestamp** - ISO format: YYYY-MM-DD HH:MM:SS

### Example Row:
```
E011,Flood,Srinagar,Jammu & Kashmir,34.0837,74.7973,High,80,50000,IMD,2025-12-15 18:00:00
```

---

## Testing Procedure

### **Test 1: File Upload**

**Using API (Recommended):**
```bash
# Step 1: Get CSRF token (login first)
# Step 2: Upload file
curl -X POST http://127.0.0.1:8000/api/data-sources/upload/ \
  -F "file=@upload_test.csv" \
  -F "source_type=csv"

# Expected response:
# {"file_path": "uploads/data_sources/abc123.csv", "original_name": "upload_test.csv", "size": 456}
```

### **Test 2: Create Data Source**

After uploading, create a DataSource record:

```bash
curl -X POST http://127.0.0.1:8000/api/data-sources/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Himalayan Disasters",
    "source_type": "csv",
    "file_path": "uploads/data_sources/abc123.csv",
    "sync_interval_minutes": 60
  }'

# Expected response:
# {"id": "uuid-here", "name": "Himalayan Disasters", "created_at": "2025-12-15T..."}
```

### **Test 3: Sync Data**

Sync the uploaded file to import events:

```bash
# Option A: Sync specific DataSource
curl -X POST http://127.0.0.1:8000/api/data-sources/{id}/sync/ \
  -H "Content-Type: application/json"

# Option B: Sync all active DataSources
curl -X POST http://127.0.0.1:8000/api/data-sources/sync_all/ \
  -H "Content-Type: application/json"

# Option C: Command line
python manage.py sync_data_sources --all
```

### **Test 4: Verify Import**

Check if data was imported:

```bash
# Check via API
curl http://127.0.0.1:8000/api/disasters/

# Expected: Should see new events in response
```

### **Test 5: View on Map**

1. Go to: `http://127.0.0.1:8000/disasters/`
2. You should see new events on the map
3. Events should be marked with colored circles
4. Click circles to see details

---

## Verification Checklist

After upload and sync:

- [ ] CSV file uploaded successfully
- [ ] DataSource record created
- [ ] Data synced without errors
- [ ] New events appear in `/api/disasters/` API
- [ ] New events visible on map at correct coordinates
- [ ] Filters work with new data
- [ ] Risk scores correctly converted
- [ ] Location names display correctly

---

## Troubleshooting

### **Upload Fails**

**Error**: "File size too large"
- Solution: Max 2.5MB - reduce CSV size

**Error**: "Invalid file format"
- Solution: Use .csv extension, check columns match expected format

**Error**: "CSRF token missing"
- Solution: Get CSRF token from login response, include in header

### **Sync Fails**

**Error**: "No file_path configured"
- Solution: Make sure file_path is set when creating DataSource

**Error**: "Could not parse CSV"
- Solution: Check CSV format, ensure proper delimiters

**Error**: "Missing required fields"
- Solution: CSV must have: disaster_type, location_name (or region+state), and coordinates

### **Data Not Showing on Map**

**Check 1**: Verify coordinates are valid
```bash
# Query API
curl http://127.0.0.1:8000/api/disasters/?risk_score_min=0
# Should see your new events with valid lat/lon
```

**Check 2**: Refresh browser (hard refresh: Ctrl+F5)

**Check 3**: Check browser console for JavaScript errors (F12)

**Check 4**: View logs for sync errors
```bash
tail -f logs/disaster_dashboard.log | grep sync
```

---

## Success Indicators

### ✅ Upload Successful
- File appears in `/api/data-sources/`
- File path shows as `uploads/data_sources/xxxxx.csv`

### ✅ Sync Successful
- Log shows: `INFO: Sync completed: X records, 0 errors`
- Events count increased in `/api/disasters/`

### ✅ Map Display Successful
- Colored circles appear on map at correct locations
- Clicking circle shows event details in popup
- Events list shows new events with "[lat, lon]" coordinates

---

## Manual Database Check

```bash
# Login to Django shell
python manage.py shell

# Check events
from disasters.models import DisasterEvent
DisasterEvent.objects.count()  # Should be increased

# Check last sync
from core.models import DataSource
ds = DataSource.objects.latest('created_at')
ds.last_sync  # Should show recent timestamp

# Check audit log
from core.models import AuditLog
AuditLog.objects.filter(action='model_change', resource_type='DataSync').last()
# Should show your sync operation
```

---

## Sample CSV Files Included

- **upload_test.csv** - 5 events from Himalayan region (ready to upload)
- **admin_disasters.csv** - 10 events from across India (already imported)

---

## Expected Results After Upload

Before:
- 10 events (from admin_disasters.csv)
- 5 locations on map

After Upload:
- 15 events (10 original + 5 new)
- 10 locations on map
- New Himalayan disaster sites visible
- All filters work with expanded dataset

---

## Next Steps

1. ✅ Find upload_test.csv file
2. ✅ Upload via admin dashboard or API
3. ✅ Create DataSource record
4. ✅ Sync data
5. ✅ Verify on map
6. ✅ Test filters with new data

Good luck with testing! 🎉
