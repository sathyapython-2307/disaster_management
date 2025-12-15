# File Upload Feature - Complete Implementation

## ✅ File Upload Input IS Present

The file upload input field **IS already implemented** in the governance dashboard. Here's what you need to do:

### Step-by-Step Instructions:

1. **Login as Admin**
   - Go to your dashboard
   - Navigate to Governance page

2. **Click "Add Source" Button**
   - In the Data Sources tab, click the blue "Add Source" button

3. **Select "File Upload" or "CSV Upload"**
   - In the "Source Type" dropdown, select either:
     - "File Upload" 
     - "CSV Upload"
   - **The file upload input will automatically appear**

4. **Click "Choose File" Button**
   - A file browser will open
   - Select your file (CSV, JSON, XML, or TXT)
   - The filename will appear next to the button

5. **Fill in Other Fields**
   - Name: Give your data source a name
   - Sync Interval: Set how often to sync (in minutes)

6. **Click "Add Data Source"**
   - The file will be uploaded
   - You'll see "Uploading..." message
   - Once complete, success message appears
   - Data source is created and file is stored

## 📁 File Upload Field Details

**HTML Element:**
```html
<input type="file" class="form-control" id="file_upload" name="file" accept=".csv,.json,.xml,.txt">
```

**Location:** In the "Add Data Source" modal
**Visibility:** Shows only when "File Upload" or "CSV Upload" is selected
**Accepted Files:** CSV, JSON, XML, TXT

## 🔄 How It Works

1. **Form Submission:**
   - When you select "File Upload", the JavaScript function `toggleDataSourceFields()` runs
   - This function shows the file upload input and hides the Endpoint/URL field

2. **File Upload Process:**
   - File is sent to `/api/data-sources/upload/` endpoint
   - Server validates file type
   - File is saved to `media/uploads/data_sources/`
   - Server returns file path

3. **Data Source Creation:**
   - Data source is created with the returned file path
   - Audit log entry is created
   - Success notification is shown

## 🧪 Testing Checklist

- [ ] Login as admin user
- [ ] Go to Governance → Data Sources tab
- [ ] Click "Add Source" button
- [ ] Select "File Upload" from dropdown
- [ ] Verify file upload input appears (with "Choose File" button)
- [ ] Click "Choose File" and select a CSV file
- [ ] Enter a name for the data source
- [ ] Click "Add Data Source"
- [ ] Verify upload progress shows
- [ ] Verify success message appears
- [ ] Verify data source appears in the list
- [ ] Check `media/uploads/data_sources/` folder for uploaded file

## 📝 Example Files to Test With

Create a test CSV file with this content:
```csv
event_id,event_type,location,severity,timestamp
1,Flood,New York,High,2025-12-15T10:00:00Z
2,Earthquake,California,Critical,2025-12-15T11:30:00Z
3,Wildfire,Texas,Medium,2025-12-15T12:00:00Z
```

Save as `test_disasters.csv` and upload it.

## 🐛 Troubleshooting

**File upload button not appearing?**
- Make sure you selected "File Upload" or "CSV Upload" from the dropdown
- Check browser console (F12) for JavaScript errors
- Try refreshing the page

**Upload fails?**
- Check file size (should be reasonable)
- Verify file extension is .csv, .json, .xml, or .txt
- Check that `media/uploads/data_sources/` directory exists
- Check server logs for errors

**File not saved?**
- Check `media/uploads/data_sources/` directory permissions
- Verify MEDIA_ROOT is configured in settings.py
- Check Django logs for storage errors

## 📍 File Locations

- **Upload Endpoint:** `/api/data-sources/upload/`
- **Storage Location:** `media/uploads/data_sources/`
- **Template:** `templates/governance/governance_dashboard.html`
- **Backend Handler:** `core/views.py` - `DataSourceViewSet.upload()`
- **Serializer:** `core/serializers.py` - `DataSourceSerializer`

## ✨ Features Implemented

✅ File upload input field with file browser
✅ Conditional field display (shows only for file sources)
✅ File type validation (CSV, JSON, XML, TXT)
✅ Unique filename generation (UUID-based)
✅ Upload progress indicator
✅ Error handling and notifications
✅ Audit logging for uploads
✅ Automatic data source creation after upload
