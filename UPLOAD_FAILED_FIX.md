# Upload Failed - Fixed

## Issue
File upload was failing with "Upload failed" error message.

## Root Cause
The file upload endpoint had an issue with how it was saving files using `default_storage.save()` with incorrect path handling.

## Solution Applied

### 1. Fixed `core/views.py` - DataSourceViewSet.upload()
**Changes:**
- Replaced `default_storage.save()` with direct file writing using `open()` and `write()`
- Fixed path handling to use `settings.MEDIA_ROOT` correctly
- Added proper error handling with try-except block
- Added logging for debugging
- Improved error messages

**Before:**
```python
full_path = default_storage.save(
    os.path.join(settings.MEDIA_ROOT, file_path),
    ContentFile(uploaded_file.read())
)
```

**After:**
```python
upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'data_sources')
os.makedirs(upload_dir, exist_ok=True)

filename = f"{uuid.uuid4()}{file_ext}"
file_full_path = os.path.join(upload_dir, filename)

with open(file_full_path, 'wb') as f:
    for chunk in uploaded_file.chunks():
        f.write(chunk)

file_path = os.path.join('uploads', 'data_sources', filename)
```

### 2. Improved Error Messages in Template
- Enhanced error display to show specific error details
- Better error message formatting in the UI

## How to Test

### Step 1: Create a Test CSV File
Create a file named `test_data.csv`:
```csv
id,name,location,severity
1,Flood,New York,High
2,Earthquake,California,Critical
3,Wildfire,Texas,Medium
```

### Step 2: Upload the File
1. Login as admin
2. Go to Governance → Data Sources
3. Click "Add Source"
4. Fill in:
   - Name: "Test Data Source"
   - Source Type: "File Upload"
5. Click "Choose File" and select `test_data.csv`
6. Click "Add Data Source"

### Step 3: Verify Success
- You should see "Uploading..." message
- Then "Data source added successfully!" message
- File should appear in the Data Sources list
- Check `media/uploads/data_sources/` folder for the uploaded file

## Troubleshooting

### If upload still fails:

**1. Check file permissions:**
```powershell
# Verify media directory exists and is writable
Get-Item -Path "media\uploads\data_sources" -Force
```

**2. Check file size:**
- Ensure file is not too large
- Django default max upload size is 2.5MB

**3. Check file extension:**
- Only CSV, JSON, XML, TXT are allowed
- Verify your file has correct extension

**4. Check Django logs:**
- Look for error messages in console
- Check for permission errors

**5. Verify MEDIA_ROOT setting:**
```python
# In disaster_dashboard/settings.py
MEDIA_ROOT = BASE_DIR / 'media'  # Should be set
MEDIA_URL = 'media/'              # Should be set
```

### Common Errors:

**"Invalid file type"**
- Solution: Use only CSV, JSON, XML, or TXT files

**"No file provided"**
- Solution: Make sure you selected a file before clicking "Add Data Source"

**"Upload failed: Permission denied"**
- Solution: Check folder permissions on `media/uploads/data_sources/`

**"Upload failed: [Errno 2] No such file or directory"**
- Solution: Ensure `media/uploads/data_sources/` directory exists
- Run: `mkdir -p media/uploads/data_sources`

## Files Modified

1. **core/views.py**
   - Fixed DataSourceViewSet.upload() method
   - Added proper error handling
   - Improved file saving logic

2. **templates/governance/governance_dashboard.html**
   - Enhanced error message display
   - Better error feedback to user

## Testing Checklist

- [ ] File upload endpoint is working
- [ ] Files are saved to correct directory
- [ ] File path is returned correctly
- [ ] Data source is created with file path
- [ ] Audit log entry is created
- [ ] Error messages are displayed correctly
- [ ] File permissions are correct
- [ ] Upload works with different file types (CSV, JSON, XML, TXT)

## Next Steps

If upload still fails after these fixes:

1. Check browser console (F12) for JavaScript errors
2. Check Django server logs for backend errors
3. Verify file is not corrupted
4. Try with a smaller test file
5. Check disk space availability

## Support

For additional help:
- Check `media/uploads/data_sources/` directory
- Review Django logs
- Verify file permissions
- Test with a simple CSV file first
