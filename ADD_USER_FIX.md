# Add User Fix - Governance Dashboard

## Issue
The "Add User" button in the governance dashboard was not working because the modal dialog was missing from the template.

## Changes Made

### 1. Updated `templates/governance/governance_dashboard.html`
- Added `#addUserModal` with a complete form for creating new users
- Added `#addGeofenceModal` for adding geofences
- Added `#addDataSourceModal` for adding data sources
- Implemented JavaScript functions:
  - `submitAddUser()` - Handles user creation via API
  - `submitAddGeofence()` - Handles geofence creation
  - `submitAddDataSource()` - Handles data source creation
  - `getCookie()` - Helper for CSRF token

### 2. Updated `core/serializers.py`
- Modified `CustomUserSerializer` to handle password field
- Added `create()` method to properly hash passwords using `set_password()`
- Added `update()` method to handle password updates
- Made password write-only for security

### 3. Updated `core/views.py`
- Added `perform_create()` method to `CustomUserViewSet` for audit logging
- Added `perform_update()` method for tracking user updates
- Both methods create audit log entries for compliance

## How It Works

1. Admin clicks "Add User" button in governance dashboard
2. Modal dialog opens with form fields:
   - Username (required)
   - Email (required)
   - First Name
   - Last Name
   - Password (required)
   - Role (dropdown: public, responder, analyst, admin)
   - Organization
   - Phone
3. On submit, JavaScript sends POST request to `/api/users/`
4. Backend creates user with hashed password
5. Audit log entry is created
6. Success notification shown and user list refreshed

## Testing
To test the fix:
1. Login as admin user
2. Navigate to Governance page
3. Click "Add User" button
4. Fill in the form and submit
5. Verify user appears in the users table
6. Check audit logs for the creation entry
