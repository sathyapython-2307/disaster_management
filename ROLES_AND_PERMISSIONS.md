# User Roles and Permissions

This document outlines the role-based access control (RBAC) system for the Disaster Risk Modeling Dashboard.

## Role Overview

The system has 4 distinct user roles with hierarchical permissions:

### 1. Administrator (admin)
**Description**: Full system access and management capabilities

**Permissions**:
- ✅ Manage users and roles
- ✅ Configure system settings
- ✅ View audit logs
- ✅ Manage geofences
- ✅ Manage data sources
- ✅ Configure alert thresholds
- ✅ View all disasters
- ✅ View all analytics
- ✅ Manage policies
- ✅ Access governance dashboard
- ✅ View compliance logs
- ✅ Manage data retention policies

**Dashboard**: Admin Dashboard
**Access Level**: Full system access

**Typical Users**: System administrators, IT staff

---

### 2. Analyst (analyst)
**Description**: Data analysis and risk assessment capabilities

**Permissions**:
- ✅ View disaster events
- ✅ Analyze risk patterns
- ✅ Generate reports
- ✅ View analytics dashboards
- ✅ Export data
- ✅ View risk models
- ✅ Access historical data
- ✅ View alert statistics

**Dashboard**: Analyst Dashboard
**Access Level**: Read-only for most resources, can export data

**Typical Users**: Data analysts, researchers, risk assessors

---

### 3. Responder (responder)
**Description**: Incident management and response coordination

**Permissions**:
- ✅ View active disaster events
- ✅ Acknowledge alerts
- ✅ Manage response actions
- ✅ Track response times
- ✅ View incident details
- ✅ Update incident status
- ✅ View active alerts

**Dashboard**: Responder Dashboard
**Access Level**: Read-write for incidents, read-only for analytics

**Typical Users**: Emergency responders, incident commanders, field coordinators

---

### 4. Public Viewer (public)
**Description**: Public information access

**Permissions**:
- ✅ View public alerts
- ✅ View public disaster information
- ✅ Access public dashboard
- ✅ View affected areas

**Dashboard**: Public Dashboard
**Access Level**: Read-only public information

**Typical Users**: General public, media, external stakeholders

---

## Role Hierarchy

```
Administrator (admin)
    ├── Can manage all roles
    ├── Can access all features
    └── Can modify system configuration

Analyst (analyst)
    ├── Can view all data
    ├── Can generate reports
    └── Can export information

Responder (responder)
    ├── Can manage incidents
    ├── Can acknowledge alerts
    └── Can coordinate response

Public Viewer (public)
    ├── Can view public information
    └── Limited read-only access
```

## Feature Access Matrix

| Feature | Admin | Analyst | Responder | Public |
|---------|-------|---------|-----------|--------|
| **User Management** | ✅ | ❌ | ❌ | ❌ |
| **System Configuration** | ✅ | ❌ | ❌ | ❌ |
| **Audit Logs** | ✅ | ❌ | ❌ | ❌ |
| **Geofence Management** | ✅ | ❌ | ❌ | ❌ |
| **Data Source Configuration** | ✅ | ❌ | ❌ | ❌ |
| **Alert Threshold Configuration** | ✅ | ❌ | ❌ | ❌ |
| **View Disasters** | ✅ | ✅ | ✅ | ✅ (public only) |
| **View Analytics** | ✅ | ✅ | ❌ | ❌ |
| **Export Reports** | ✅ | ✅ | ❌ | ❌ |
| **Acknowledge Alerts** | ✅ | ❌ | ✅ | ❌ |
| **Manage Incidents** | ✅ | ❌ | ✅ | ❌ |
| **View Audit Trail** | ✅ | ❌ | ❌ | ❌ |
| **Manage Policies** | ✅ | ❌ | ❌ | ❌ |
| **View Public Alerts** | ✅ | ✅ | ✅ | ✅ |

## Dashboard Access

| Dashboard | Admin | Analyst | Responder | Public |
|-----------|-------|---------|-----------|--------|
| Admin Dashboard | ✅ | ❌ | ❌ | ❌ |
| Analyst Dashboard | ❌ | ✅ | ❌ | ❌ |
| Responder Dashboard | ❌ | ❌ | ✅ | ❌ |
| Public Dashboard | ❌ | ❌ | ❌ | ✅ |
| Governance | ✅ | ❌ | ❌ | ❌ |

## API Endpoint Access

### User Management Endpoints
- `GET /api/users/` - Admin only
- `POST /api/users/` - Admin only
- `PUT /api/users/{id}/` - Admin only
- `DELETE /api/users/{id}/` - Admin only
- `POST /api/users/{id}/change_role/` - Admin only
- `GET /api/users/me/` - All authenticated users

### Disaster Endpoints
- `GET /api/disasters/` - Admin, Analyst, Responder
- `GET /api/disasters/active_events/` - Admin, Analyst, Responder
- `GET /api/disasters/high_risk/` - Admin, Analyst, Responder
- `POST /api/disasters/{id}/update_status/` - Admin, Responder

### Alert Endpoints
- `GET /api/alerts/` - All authenticated users
- `GET /api/alerts/pending/` - All authenticated users
- `POST /api/alerts/{id}/acknowledge/` - Admin, Responder
- `GET /api/alert-thresholds/` - Admin only
- `POST /api/alert-thresholds/` - Admin only

### Analytics Endpoints
- `GET /api/disaster-analytics/` - Admin, Analyst
- `GET /api/alert-analytics/` - Admin, Analyst
- `GET /api/system-metrics/` - Admin only

### Governance Endpoints
- `GET /api/role-permissions/` - Admin only
- `POST /api/role-permissions/` - Admin only
- `GET /api/policies/` - Admin only
- `POST /api/policies/` - Admin only
- `GET /api/compliance-logs/` - Admin only
- `GET /api/retention-policies/` - Admin only

## Role Assignment

### Creating Users with Specific Roles

**Via Admin Panel**:
1. Go to `/admin/`
2. Click "Users"
3. Click "Add User"
4. Fill in user details
5. Select role from dropdown
6. Save

**Via API**:
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "analyst1",
    "email": "analyst1@example.com",
    "password": "securepassword",
    "role": "analyst"
  }'
```

**Via Management Command**:
```bash
python manage.py populate_initial_data
```

### Changing User Roles

**Via Admin Panel**:
1. Go to `/admin/`
2. Click "Users"
3. Select user
4. Change role
5. Save

**Via API**:
```bash
curl -X POST http://localhost:8000/api/users/{user_id}/change_role/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "analyst"}'
```

## Permission Checking in Code

### Using Decorators

```python
from core.permissions import require_role, require_permission, ADMIN, ANALYST

# Restrict to admin only
@require_role(ADMIN)
def admin_only_view(request):
    pass

# Restrict to admin or analyst
@require_role(ADMIN, ANALYST)
def admin_or_analyst_view(request):
    pass

# Check specific permission
@require_permission('manage_users')
def manage_users_view(request):
    pass
```

### Using Permission Classes

```python
from rest_framework import viewsets
from core.permissions import IsAdmin, IsAdminOrAnalyst

class AdminOnlyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]

class AdminOrAnalystViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAnalyst]
```

### Checking Permissions in Views

```python
from core.permissions import check_role_permission

def my_view(request):
    if check_role_permission(request.user, 'manage_users'):
        # User has permission
        pass
    else:
        # User doesn't have permission
        pass
```

## Security Best Practices

1. **Principle of Least Privilege**: Assign users the minimum role needed
2. **Regular Audits**: Review user roles and permissions regularly
3. **Audit Logging**: All role changes are logged in audit trail
4. **Role Separation**: Separate duties between roles
5. **Access Control**: Enforce role-based access at all levels
6. **Monitoring**: Monitor access patterns for anomalies

## Default Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Analyst | analyst_user | password123 |
| Responder | responder_user | password123 |
| Public | public_user | password123 |

**Note**: Change these credentials in production!

## Audit Trail

All role changes and permission-related actions are logged in the audit trail:

```
GET /api/audit-logs/?action=update&resource_type=User
```

## Troubleshooting

### User Can't Access Feature
1. Check user's role: `GET /api/users/me/`
2. Verify role has permission for feature
3. Check audit logs for access attempts
4. Contact admin to update role if needed

### Permission Denied Error
1. Verify you're logged in
2. Check your user role
3. Verify the feature is available for your role
4. Contact admin if you need additional permissions

### Role Change Not Taking Effect
1. Log out and log back in
2. Clear browser cache
3. Check audit logs to confirm change was saved
4. Verify in admin panel

## Support

For role and permission issues, contact your system administrator.
