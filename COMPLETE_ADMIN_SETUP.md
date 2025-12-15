# Complete Admin Setup & User Management Guide

## Quick Start - Add Your First User

### 1. Login to Admin Panel
```
URL: http://localhost:8000/admin/
Username: admin
Password: admin123
```

### 2. Navigate to Users
- Look for "CORE" section in left sidebar
- Click "Users"

### 3. Click "+ Add User" Button
- Button is in top right corner
- Opens the user creation form

### 4. Fill in the Form

#### Required Fields:
```
Username: (unique identifier)
Password: (at least 8 characters)
Password confirmation: (must match)
Email: (valid email address)
Role: (select from dropdown)
```

#### Optional Fields:
```
First name: (user's first name)
Last name: (user's last name)
Organization: (company/organization)
Phone: (contact number)
```

### 5. Click "Save"
- User is created
- You'll see success message
- User can now login

---

## User Roles Explained

### Admin
- **Full system access**
- Can manage everything
- Can create/edit/delete users
- Can configure system
- Can view all data

### Analyst
- **Data analysis access**
- Can view disasters
- Can view analytics
- Can export reports
- Cannot manage users

### Responder
- **Incident management**
- Can view active incidents
- Can acknowledge alerts
- Can manage response
- Cannot view analytics

### Public Viewer
- **Read-only public access**
- Can view public alerts
- Can view public disasters
- Cannot manage anything
- Limited information access

---

## Complete User Management

### View All Users
1. Go to Admin: `http://localhost:8000/admin/`
2. Click "Users"
3. See list of all users

### Edit User
1. Click on username in list
2. Modify fields
3. Click "Save"

### Change User Role
1. Click on username
2. Change "Role" dropdown
3. Click "Save"

### Delete User
1. Click on username
2. Click "Delete" button
3. Confirm deletion

### Search Users
1. Use search box at top
2. Search by username, email, or organization

### Filter Users
1. Use filters on right side
2. Filter by role or active status

---

## Admin Features

### 1. User Management
- ✅ Add users
- ✅ Edit users
- ✅ Delete users
- ✅ Change roles
- ✅ View user details

### 2. Disaster Management
- ✅ Add disaster events
- ✅ Edit events
- ✅ Delete events
- ✅ View event details
- ✅ Track event status

### 3. Alert Management
- ✅ Create alerts
- ✅ Configure thresholds
- ✅ Manage alert dispatch
- ✅ View alert history

### 4. Data Source Management
- ✅ Add data sources
- ✅ Configure connections
- ✅ Manage API keys
- ✅ Set sync intervals

### 5. Geofence Management
- ✅ Create geofences
- ✅ Define boundaries
- ✅ Associate disaster types
- ✅ Enable/disable geofences

### 6. System Configuration
- ✅ Configure system settings
- ✅ Set thresholds
- ✅ Manage policies
- ✅ View audit logs

---

## Admin Dashboard Features

### Statistics
- Active events count
- Critical alerts count
- Active users count
- System health status

### Quick Actions
- Manage system
- View analytics
- View alerts
- Access governance

### Recent Events
- View latest events
- See recent changes
- Track system activity

---

## Governance Features

### User & Role Management
- Manage users
- Assign roles
- Configure permissions
- View user activity

### System Configuration
- Configure geofences
- Manage data sources
- Set alert thresholds
- Configure policies

### Audit & Compliance
- View audit logs
- Track all changes
- Monitor user actions
- Compliance reporting

### Data Management
- Set retention policies
- Archive old data
- Manage data sources
- Configure backups

---

## Common Tasks

### Task 1: Add New Analyst
```
1. Go to Admin → Users
2. Click "+ Add User"
3. Username: analyst_name
4. Password: SecurePass123!
5. Email: analyst@company.com
6. Role: analyst
7. Click Save
```

### Task 2: Add New Responder
```
1. Go to Admin → Users
2. Click "+ Add User"
3. Username: responder_name
4. Password: SecurePass123!
5. Email: responder@company.com
6. Role: responder
7. Click Save
```

### Task 3: Upgrade User to Admin
```
1. Go to Admin → Users
2. Click on user
3. Change Role to: admin
4. Click Save
```

### Task 4: Create Geofence
```
1. Go to Admin → Geofences
2. Click "+ Add Geofence"
3. Name: City Name
4. Coordinates: [lat, lng]
5. Disaster types: flood, earthquake
6. Click Save
```

### Task 5: Add Data Source
```
1. Go to Admin → Data Sources
2. Click "+ Add Data Source"
3. Name: API Name
4. Type: api
5. Endpoint: https://api.example.com
6. API Key: your_key
7. Click Save
```

### Task 6: Configure Alert Threshold
```
1. Go to Admin → Alert Thresholds
2. Click "+ Add Alert Threshold"
3. Disaster type: flood
4. Risk threshold: 70
5. Confidence threshold: 75
6. Channels: email, push
7. Click Save
```

---

## Troubleshooting

### Issue: Can't Add User
**Solution**: 
- Clear browser cache (Ctrl+Shift+Delete)
- Refresh page (F5)
- Try direct URL: `http://localhost:8000/admin/core/customuser/add/`

### Issue: Form Won't Submit
**Solution**:
- Check all required fields are filled
- Check passwords match
- Check email format is valid
- Check username is unique

### Issue: Permission Denied
**Solution**:
- Make sure you're logged in as admin
- Check your user role is "admin"
- Try logging out and back in

### Issue: Database Error
**Solution**:
- Run: `python manage.py migrate`
- Run: `python manage.py check`
- Restart Django server

---

## Security Best Practices

### ✅ DO:
- Use strong passwords (8+ characters, mix of types)
- Change default admin password
- Assign minimum required role
- Review users regularly
- Monitor audit logs
- Enable 2FA if available
- Use HTTPS in production
- Backup database regularly

### ❌ DON'T:
- Share admin credentials
- Use simple passwords
- Give admin role to everyone
- Leave unused accounts active
- Ignore audit logs
- Store passwords in plain text
- Use HTTP in production
- Skip backups

---

## Admin Checklist

- ✅ Login as admin
- ✅ Change admin password
- ✅ Create analyst users
- ✅ Create responder users
- ✅ Configure geofences
- ✅ Add data sources
- ✅ Set alert thresholds
- ✅ Configure policies
- ✅ Review audit logs
- ✅ Test all features

---

## Support

### If you need help:
1. Check this guide
2. Check troubleshooting section
3. Check browser console (F12)
4. Check server logs
5. Share error message

### Contact:
- Check README.md for support info
- Review error logs
- Check documentation

---

## Status

✅ **Admin Panel is Fully Functional!**

You can now:
- Add users with different roles
- Manage system configuration
- Configure alerts and thresholds
- Manage geofences and data sources
- View audit logs
- Access all governance features

**Ready to use!** 🚀
