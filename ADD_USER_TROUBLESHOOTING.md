# Add User - Troubleshooting Guide

## Issue: "Add User" Button Not Working

If clicking the "+ Add User" button doesn't open the form, try these solutions:

---

## Solution 1: Clear Browser Cache

### Steps:
1. **Press Ctrl+Shift+Delete** (or Cmd+Shift+Delete on Mac)
2. Select "All time" for time range
3. Check "Cookies and other site data"
4. Check "Cached images and files"
5. Click "Clear data"
6. Refresh the page

### Or:
1. Go to `http://localhost:8000/admin/`
2. Press **F5** to refresh
3. Try clicking "+ Add User" again

---

## Solution 2: Check Browser Console for Errors

### Steps:
1. Press **F12** to open Developer Tools
2. Click "Console" tab
3. Look for any red error messages
4. Take a screenshot and share the error

### Common Errors:
- **CSRF token missing** - Refresh page
- **404 Not Found** - Check URL
- **Permission denied** - Make sure you're logged in as admin

---

## Solution 3: Verify Admin Access

### Check:
1. Are you logged in as **admin**?
2. Is your user role set to **admin**?
3. Can you see other admin pages?

### Test:
```
Go to: http://localhost:8000/admin/
You should see: "Django administration"
```

---

## Solution 4: Try Direct URL

### Instead of clicking the button, try:
```
http://localhost:8000/admin/core/customuser/add/
```

This should open the add user form directly.

---

## Solution 5: Check Server Logs

### Look for errors in terminal:
```
[15/Dec/2025 11:47:40] "GET /admin/core/customuser/add/ HTTP/1.1" 200
```

If you see **500** instead of **200**, there's a server error.

### Share the full error message from terminal.

---

## Solution 6: Restart Django Server

### Steps:
1. Stop the server (Ctrl+C)
2. Run: `.venv\Scripts\Activate.ps1`
3. Run: `python manage.py runserver`
4. Try adding user again

---

## Solution 7: Check Database

### Verify database is working:
```bash
.venv\Scripts\Activate.ps1
python manage.py shell
>>> from core.models import CustomUser
>>> CustomUser.objects.all()
<QuerySet [<CustomUser: admin (Administrator)>]>
```

If you get an error, the database might be corrupted.

---

## Solution 8: Verify Admin Registration

### Check if CustomUserAdmin is registered:
```bash
.venv\Scripts\Activate.ps1
python manage.py shell
>>> from django.contrib import admin
>>> from core.models import CustomUser
>>> admin.site._registry[CustomUser]
<core.admin.CustomUserAdmin object at 0x...>
```

If you get an error, the admin is not registered.

---

## Solution 9: Check Form Validation

### When you click "Add User", you might see validation errors:

| Error | Solution |
|-------|----------|
| "This field is required" | Fill in all required fields |
| "Username already exists" | Choose a different username |
| "Enter a valid email" | Use format: user@example.com |
| "Passwords don't match" | Make sure both passwords are identical |

---

## Solution 10: Manual User Creation via Shell

### If the admin form doesn't work, create user via shell:

```bash
.venv\Scripts\Activate.ps1
python manage.py shell
```

Then run:
```python
from core.models import CustomUser

user = CustomUser.objects.create_user(
    username='john_analyst',
    email='john@example.com',
    password='SecurePass123!',
    role='analyst',
    first_name='John',
    last_name='Doe',
    organization='Company'
)
print(f"User created: {user}")
```

---

## Step-by-Step: Adding User (Detailed)

### Step 1: Login
```
URL: http://localhost:8000/login/
Username: admin
Password: admin123
```

### Step 2: Go to Admin
```
URL: http://localhost:8000/admin/
```

### Step 3: Click Users
You should see "Users" in the left sidebar under "Core"

### Step 4: Click "+ Add User" Button
The button is in the top right corner

### Step 5: Fill Form

**Section 1: Username & Password**
```
Username: john_analyst
Password: SecurePass123!
Password confirmation: SecurePass123!
```

**Section 2: Personal Info**
```
First name: John
Last name: Doe
Email: john@example.com
```

**Section 3: Role Assignment**
```
Role: analyst
Organization: Company
Phone: +1-555-0123
```

### Step 6: Save
Click "Save" button at bottom right

### Expected Result:
```
User "john_analyst" was added successfully.
```

---

## If Still Not Working

### Please provide:
1. **Screenshot** of the error
2. **Browser console errors** (F12 → Console)
3. **Server terminal output** (full error message)
4. **Your admin username** (confirm you're logged in as admin)
5. **Steps you took** before the error

### Then run:
```bash
.venv\Scripts\Activate.ps1
python manage.py check
python manage.py migrate --check
```

And share the output.

---

## Quick Checklist

- ✅ Logged in as admin?
- ✅ Browser cache cleared?
- ✅ Server running?
- ✅ No console errors?
- ✅ Database working?
- ✅ Admin registered?
- ✅ Form fields visible?
- ✅ Can submit form?

---

## Alternative: Use API to Add User

If admin panel doesn't work, use the API:

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_analyst",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "role": "analyst",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

---

## Status

If you follow these steps, the "Add User" feature should work! 

**If it still doesn't work, please share:**
- Screenshot of the issue
- Browser console errors
- Server terminal output
- Your admin credentials confirmation

Then I can provide more specific help! 🚀
