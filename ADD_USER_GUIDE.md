# How to Add Users in Admin Panel

## Fixed Issue ✅
The "Add User" button in the admin panel now works correctly!

---

## Step-by-Step Guide to Add a User

### Step 1: Login as Admin
```
URL: http://localhost:8000/login/
Username: admin
Password: admin123
```

### Step 2: Go to Admin Panel
```
URL: http://localhost:8000/admin/
```

### Step 3: Click on "Users"
You'll see the Users section in the admin panel.

### Step 4: Click "Add User" Button
Click the green "+ Add User" button in the top right.

### Step 5: Fill in User Information

#### Section 1: Username and Password
- **Username**: Enter a unique username (e.g., `john_analyst`)
- **Password**: Enter a secure password
- **Password confirmation**: Re-enter the password

#### Section 2: Personal Information
- **First name**: Enter first name (e.g., `John`)
- **Last name**: Enter last name (e.g., `Doe`)
- **Email**: Enter email address (e.g., `john@example.com`)

#### Section 3: Role Assignment
- **Role**: Select one of:
  - `admin` - Administrator (full access)
  - `analyst` - Analyst (data analysis access)
  - `responder` - Responder (incident management)
  - `public` - Public Viewer (read-only public access)
- **Organization**: Enter organization name (optional)
- **Phone**: Enter phone number (optional)

### Step 6: Save User
Click the "Save" button at the bottom right.

---

## Example: Adding an Analyst User

### Form Fields:
```
Username: analyst_john
Password: SecurePass123!
Password confirmation: SecurePass123!
First name: John
Last name: Smith
Email: john.smith@company.com
Role: analyst
Organization: Emergency Management
Phone: +1-555-0123
```

### Result:
User created successfully! ✅

---

## Example: Adding a Responder User

### Form Fields:
```
Username: responder_mary
Password: SecurePass456!
Password confirmation: SecurePass456!
First name: Mary
Last name: Johnson
Email: mary.johnson@company.com
Role: responder
Organization: Fire Department
Phone: +1-555-0456
```

### Result:
User created successfully! ✅

---

## Example: Adding a Public Viewer User

### Form Fields:
```
Username: public_viewer
Password: SecurePass789!
Password confirmation: SecurePass789!
First name: Public
Last name: User
Email: public@example.com
Role: public
Organization: General Public
Phone: +1-555-0789
```

### Result:
User created successfully! ✅

---

## User Roles Explained

### Admin Role
- **Access**: Full system access
- **Permissions**:
  - Manage users
  - Configure system
  - View audit logs
  - Manage geofences
  - Manage data sources
  - Configure alerts
  - View all data

### Analyst Role
- **Access**: Data analysis and reporting
- **Permissions**:
  - View disasters
  - View analytics
  - Export reports
  - View risk models
  - Access historical data

### Responder Role
- **Access**: Incident management
- **Permissions**:
  - View active incidents
  - Acknowledge alerts
  - Manage response actions
  - Track response times
  - Update incident status

### Public Viewer Role
- **Access**: Public information only
- **Permissions**:
  - View public alerts
  - View public disaster information
  - Access public dashboard
  - View affected areas

---

## After Creating a User

### The user can now:
1. **Login** at `http://localhost:8000/login/`
2. **Use their credentials**:
   - Username: (as entered)
   - Password: (as entered)
3. **Access their role-specific dashboard**
4. **Perform role-specific actions**

---

## Changing User Role

### To change a user's role:

1. Go to Admin Panel: `http://localhost:8000/admin/`
2. Click "Users"
3. Click on the user you want to modify
4. Change the "Role" field
5. Click "Save"

---

## Deleting a User

### To delete a user:

1. Go to Admin Panel: `http://localhost:8000/admin/`
2. Click "Users"
3. Click on the user you want to delete
4. Click "Delete" button at the bottom
5. Confirm deletion

---

## Troubleshooting

### Issue: "Add User" button doesn't work
**Solution**: Make sure you're logged in as admin and have admin permissions.

### Issue: Password validation error
**Solution**: Password must be at least 8 characters and not be entirely numeric.

### Issue: Username already exists
**Solution**: Choose a different username. Usernames must be unique.

### Issue: Email validation error
**Solution**: Enter a valid email address (e.g., user@example.com).

---

## Quick Reference

| Field | Required | Example |
|-------|----------|---------|
| Username | Yes | john_analyst |
| Password | Yes | SecurePass123! |
| First Name | No | John |
| Last Name | No | Doe |
| Email | Yes | john@example.com |
| Role | Yes | analyst |
| Organization | No | Company Name |
| Phone | No | +1-555-0123 |

---

## Security Tips

1. ✅ Use strong passwords (mix of letters, numbers, symbols)
2. ✅ Don't share passwords
3. ✅ Change default passwords
4. ✅ Assign minimum required role
5. ✅ Review users regularly
6. ✅ Disable inactive users

---

## Status

✅ **Add User Feature is Working!**

You can now successfully add users with different roles in the admin panel.
