# Quick Start Guide - Disaster Risk Modeling Dashboard

## Prerequisites
- Python 3.8+
- Virtual environment activated
- Dependencies installed

## Running the Application

### 1. Activate Virtual Environment
```bash
# Windows
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

### 2. Start Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

### 3. Login with Default Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | admin | admin123 |
| **Analyst** | analyst_user | password123 |
| **Responder** | responder_user | password123 |
| **Public** | public_user | password123 |

## Key URLs

| Page | URL | Role |
|------|-----|------|
| Login | http://localhost:8000/login/ | All |
| Register | http://localhost:8000/register/ | All |
| Dashboard | http://localhost:8000/ | All |
| Disasters Map | http://localhost:8000/disasters/ | Analyst, Responder, Admin |
| Alerts | http://localhost:8000/alerts/ | All |
| Analytics | http://localhost:8000/analytics/ | Analyst, Admin |
| Governance | http://localhost:8000/governance/ | Admin |
| Admin Panel | http://localhost:8000/admin/ | Admin |

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### Common Endpoints
- `GET /api/users/` - List users
- `GET /api/disasters/` - List disasters
- `GET /api/alerts/` - List alerts
- `GET /api/audit-logs/` - View audit trail
- `GET /api/disaster-analytics/` - Analytics data
- `GET /api/system-metrics/` - System health

### Authentication
All API endpoints require authentication. Use session authentication or add `Authorization` header.

## Database Management

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Populate Initial Data
```bash
python manage.py populate_initial_data
```

### Create Superuser
```bash
python manage.py createsuperuser
```

## Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test core
python manage.py test disasters
python manage.py test alerts
```

### Run with Verbosity
```bash
python manage.py test --verbosity=2
```

## Project Structure

```
disaster_dashboard/
├── core/              # User management, audit logs
├── disasters/         # Disaster events, risk models
├── alerts/            # Alert system, notifications
├── analytics/         # Analytics, reporting
├── governance/        # Administration, compliance
├── templates/         # HTML templates
├── static/            # CSS, JavaScript
└── manage.py          # Django management
```

## Features by Role

### Admin
- ✅ Manage users and roles
- ✅ Configure system settings
- ✅ View audit logs
- ✅ Manage geofences
- ✅ Configure data sources
- ✅ Set alert thresholds
- ✅ View all analytics

### Analyst
- ✅ View disaster events
- ✅ Analyze risk patterns
- ✅ Generate reports
- ✅ View analytics
- ✅ Export data

### Responder
- ✅ View active incidents
- ✅ Acknowledge alerts
- ✅ Manage response actions
- ✅ Track response times

### Public Viewer
- ✅ View public alerts
- ✅ View disaster information
- ✅ Access public dashboard

## Common Tasks

### Add a New User
1. Go to Admin Panel (`/admin/`)
2. Click "Users"
3. Click "Add User"
4. Fill in details and select role
5. Save

### Create a Geofence
1. Go to Governance (`/governance/`)
2. Click "Geofences" tab
3. Click "Add Geofence"
4. Define area and disaster types
5. Save

### Configure Alert Threshold
1. Go to Governance (`/governance/`)
2. Click "Roles & Permissions" tab
3. Set risk score and confidence thresholds
4. Select notification channels
5. Save

### View Audit Trail
1. Go to Governance (`/governance/`)
2. Click "Audit Logs" tab
3. Filter by user, action, or date
4. View detailed logs

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Locked
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Clear Cache
```bash
python manage.py clear_cache
```

## Environment Variables

Create a `.env` file in the project root:

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Performance Tips

1. Use pagination for large datasets
2. Filter data before loading
3. Use browser cache for static files
4. Monitor system metrics
5. Archive old data regularly

## Security Reminders

- ✅ Change default passwords
- ✅ Set `DEBUG=False` in production
- ✅ Use strong `SECRET_KEY`
- ✅ Enable HTTPS
- ✅ Configure ALLOWED_HOSTS
- ✅ Use environment variables for secrets
- ✅ Regular backups
- ✅ Monitor audit logs

## Support & Documentation

- Full documentation: See `README.md`
- API documentation: See `README.md` - API Endpoints section
- Deployment guide: See `README.md` - Deployment section

## Next Steps

1. ✅ Start the server
2. ✅ Login with admin credentials
3. ✅ Explore the dashboards
4. ✅ Create sample data
5. ✅ Configure alerts
6. ✅ Test notifications
7. ✅ Review audit logs
8. ✅ Deploy to production

---

**Happy Disaster Monitoring! 🚀**
