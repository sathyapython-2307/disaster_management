# Data Source File Upload Fix

## Issue
When selecting "File" as the source type in the "Add Data Source" modal, the system was asking for an "Endpoint/URL" instead of providing a file upload button.

## Root Cause
1. The DataSource model didn't have a field for file paths
2. The modal form didn't have a file upload input
3. No backend endpoint existed to handle file uploads
4. The source type choices in the model didn't match the form options

## Changes Made

### 1. Updated `core/models.py`
- Added `file_path` field to DataSource model for storing uploaded file locations
- Changed `endpoint` field to allow null values (not required for file sources)
- Updated SOURCE_TYPES to include all relevant options:
  - `api` - API
  - `csv` - CSV Upload
  - `file` - File Upload
  - `database` - Database
  - `sensor` - Sensor Network
  - `satellite` - Satellite Data
  - `weather` - Weather Service
  - `stream` - Data Stream

### 2. Updated `core/serializers.py`
- Added `file_path` to DataSourceSerializer fields
- Added validation logic:
  - For file/csv sources: requires `file_path`
  - For api/database/weather/stream sources: requires `endpoint`
  - For other sources: both fields are optional

### 3. Updated `core/views.py`
- Added `upload()` action to DataSourceViewSet
- Handles file uploads via `/api/data-sources/upload/`
- Features:
  - Validates file types (CSV, JSON, XML, TXT)
  - Generates unique filenames using UUID
  - Saves files to `media/uploads/data_sources/`
  - Creates audit log entries for uploads
  - Returns file path for data source creation

### 4. Updated `templates/governance/governance_dashboard.html`
- Changed form to support file uploads (`enctype="multipart/form-data"`)
- Added file upload input with accept filter for allowed file types
- Added `toggleDataSourceFields()` JavaScript function to show/hide fields
- Updated `submitAddDataSource()` to handle two-step process:
  1. Upload file to server
  2. Create data source with returned file path
- Added upload progress indicator
- Made Endpoint/URL field conditional (shows only for API, Database, Weather, Stream)
- Added File Upload field (shows only for File and CSV sources)

### 5. Created Upload Directory
- Created `media/uploads/data_sources/` directory for storing uploaded files

### 6. Database Migration
- Created and applied migration: `0002_datasource_file_path_alter_datasource_endpoint_and_more.py`

## How It Works Now

1. Admin opens "Add Data Source" modal
2. Selects a source type from dropdown
3. Form dynamically shows relevant fields:
   - **File/CSV sources**: Shows file upload button with browse capability
   - **API/Database/Weather/Stream sources**: Shows "Endpoint/URL" text field (required)
   - **Other sources**: Shows "Endpoint/URL" field (optional)
4. For file uploads:
   - User clicks "Choose File" and selects a file from their computer
   - Accepted formats: CSV, JSON, XML, TXT
   - On submit, file is uploaded first
   - Server saves file with unique name
   - Data source is created with the file path
5. Upload progress is shown with spinner
6. Success/error notifications are displayed

## Example Usage

### For File Upload:
1. Name: "Disaster Events CSV"
2. Source Type: "File Upload"
3. Click "Choose File" and select your CSV file
4. Sync Interval: 60 minutes
5. Click "Add Data Source"
6. File is uploaded and data source is created

### For API:
1. Name: "Weather API"
2. Source Type: "API"
3. Endpoint/URL: "https://api.weather.gov/data"
4. Sync Interval: 15 minutes
5. Click "Add Data Source"

## API Endpoints

### Upload File
- **URL**: `/api/data-sources/upload/`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: 
  - `file`: File to upload
  - `source_type`: Type of source (file/csv)
- **Response**: 
  ```json
  {
    "file_path": "uploads/data_sources/uuid.csv",
    "original_name": "disasters.csv",
    "size": 12345
  }
  ```

### Create Data Source
- **URL**: `/api/data-sources/`
- **Method**: POST
- **Content-Type**: application/json
- **Body**:
  ```json
  {
    "name": "Disaster Events CSV",
    "source_type": "file",
    "file_path": "uploads/data_sources/uuid.csv",
    "sync_interval_minutes": 60
  }
  ```

## Testing
1. Login as admin
2. Go to Governance page → Data Sources tab
3. Click "Add Source"
4. Select "File Upload" - verify file upload button appears
5. Click "Choose File" and select a CSV file
6. Fill in name and click "Add Data Source"
7. Verify upload progress is shown
8. Verify success message and data source appears in list
9. Check `media/uploads/data_sources/` for uploaded file
10. Check audit logs for upload entry
