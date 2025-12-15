# Upload Error: "Unexpected token '<'" - Debugging Guide

## What This Error Means

The error "Unexpected token '<'" indicates that the server is returning **HTML** instead of **JSON**. This typically happens when:

1. The endpoint returns a 404 error page (HTML)
2. The endpoint returns a 500 error page (HTML)
3. The endpoint URL is incorrect
4. The request is being redirected

## Root Cause Analysis

The issue was that the response error handling wasn't properly checking the content type before trying to parse as JSON.

## Fixes Applied

### 1. Fixed `core/views.py`
- Removed incorrect `permission_classes` parameter from `@action` decorator
- The decorator now uses the viewset's default permission classes

### 2. Improved `templates/governance/governance_dashboard.html`
- Added content-type checking before parsing JSON
- Better error message handling
- Improved error logging

## How to Debug

### Step 1: Check Browser Console
1. Open browser (F12)
2. Go to Console tab
3. Try uploading a file
4. Look for error messages
5. Check Network tab to see the actual response

### Step 2: Check Network Request
1. Open Developer Tools (F12)
2. Go to Network tab
3. Try uploading a file
4. Look for the `/api/data-sources/upload/` request
5. Click on it and check:
   - Status code (should be 200)
   - Response headers (should have `Content-Type: application/json`)
   - Response body (should be JSON, not HTML)

### Step 3: Check Django Logs
Run the server and watch for errors:
```bash
python manage.py runserver
```

Look for error messages related to:
- File upload
- Permission denied
- File not found
- Invalid path

### Step 4: Verify Endpoint URL
The endpoint should be: `/api/data-sources/upload/`

Check that:
- URL is correct
- CSRF token is being sent
- Request method is POST
- Content-Type is multipart/form-data

## Common Issues and Solutions

### Issue 1: 404 Error (Endpoint Not Found)
**Symptoms:**
- Network tab shows 404 status
- Response is HTML error page

**Solutions:**
1. Verify the endpoint URL is `/api/data-sources/upload/`
2. Check that DataSourceViewSet is registered in router
3. Verify the `upload` method exists in DataSourceViewSet
4. Restart Django server

### Issue 2: 403 Forbidden (Permission Denied)
**Symptoms:**
- Network tab shows 403 status
- Error message about permissions

**Solutions:**
1. Make sure you're logged in as admin
2. Check that user has proper permissions
3. Verify CSRF token is being sent

### Issue 3: 500 Internal Server Error
**Symptoms:**
- Network tab shows 500 status
- Django logs show error traceback

**Solutions:**
1. Check Django logs for specific error
2. Verify media directory exists and is writable
3. Check file permissions
4. Verify file extension is allowed

### Issue 4: File Not Saved
**Symptoms:**
- Upload appears successful
- File not found in media/uploads/data_sources/

**Solutions:**
1. Check directory permissions
2. Verify MEDIA_ROOT is set correctly
3. Check disk space
4. Verify file path is correct

## Testing Steps

### Test 1: Simple File Upload
1. Create a test CSV file:
```csv
id,name,value
1,Test,100
2,Data,200
```

2. Save as `test.csv`

3. Go to Governance → Data Sources

4. Click "Add Source"

5. Fill in:
   - Name: "Test Upload"
   - Source Type: "File Upload"

6. Click "Choose File" and select `test.csv`

7. Click "Add Data Source"

8. Check:
   - Browser console for errors
   - Network tab for response
   - Django logs for errors
   - media/uploads/data_sources/ for file

### Test 2: Check Endpoint Directly
Using curl or Postman:
```bash
curl -X POST http://localhost:8000/api/data-sources/upload/ \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -F "file=@test.csv" \
  -F "source_type=file"
```

Expected response:
```json
{
  "file_path": "uploads/data_sources/uuid.csv",
  "original_name": "test.csv",
  "size": 123
}
```

## Files Modified

1. **core/views.py**
   - Fixed `@action` decorator
   - Improved error handling

2. **templates/governance/governance_dashboard.html**
   - Added content-type checking
   - Better error messages
   - Improved error logging

## Next Steps

If upload still fails:

1. **Check Django logs** - Run server and watch for errors
2. **Check browser console** - Look for JavaScript errors
3. **Check network tab** - Verify request/response
4. **Test endpoint directly** - Use curl or Postman
5. **Check file permissions** - Verify media directory is writable
6. **Check disk space** - Ensure enough space for uploads

## Support Information

**Endpoint:** `/api/data-sources/upload/`
**Method:** POST
**Content-Type:** multipart/form-data
**Required Fields:** file, source_type
**Response:** JSON with file_path, original_name, size

**Upload Directory:** `media/uploads/data_sources/`
**Allowed Extensions:** .csv, .json, .xml, .txt
**Max File Size:** 2.5MB (Django default)

## Quick Checklist

- [ ] Django server is running
- [ ] You're logged in as admin
- [ ] File is CSV, JSON, XML, or TXT
- [ ] File size is under 2.5MB
- [ ] media/uploads/data_sources/ directory exists
- [ ] Directory has write permissions
- [ ] CSRF token is being sent
- [ ] Endpoint URL is correct
- [ ] Browser console shows no errors
- [ ] Network tab shows 200 status
