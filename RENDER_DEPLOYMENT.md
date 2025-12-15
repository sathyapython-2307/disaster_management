# Render Deployment Guide

## Files Created for Deployment

### 1. **Procfile**
Specifies the command to run your Django application on Render:
```
web: gunicorn disaster_dashboard.wsgi:application
```

### 2. **render.yaml**
Render's infrastructure-as-code configuration file that defines:
- Service type: web (Python 3.11)
- Build command: Install dependencies and collect static files
- Start command: Run Gunicorn WSGI server
- Environment variables for production

### 3. **requirements.txt** (Updated)
Removed version specifications - includes:
- Django
- djangorestframework
- django-cors-headers
- django-filter
- Pillow
- python-decouple
- requests
- pytz
- **gunicorn** (new - WSGI server)
- **whitenoise** (new - static file serving)

### 4. **runtime.txt**
Specifies Python version: `python-3.11.7`

### 5. **build.sh**
Build script that Render executes:
- Upgrades pip
- Installs requirements
- Collects static files with `collectstatic`
- Runs migrations

### 6. **Settings Configuration Updates**

#### Security Settings (Production-Ready)
```python
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']  # Render domains will be added
SECRET_KEY = config('SECRET_KEY', default=...)  # Use environment variable
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

#### Whitenoise Middleware
Added for efficient static file serving:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # New
    ...
]

# Whitenoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Deployment Steps on Render

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Connect to Render
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Select `disaster_management_realtime` repository

### 3. Configure Service on Render

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```
gunicorn disaster_dashboard.wsgi:application
```

### 4. Set Environment Variables
In Render dashboard → Environment:
```
DEBUG = false
SECRET_KEY = your-secret-key-here
ALLOWED_HOSTS = your-render-domain.onrender.com
```

### 5. Deploy
- Click "Create Web Service"
- Render will automatically build and deploy
- Monitor logs in Render dashboard

## Important Notes

### Static Files
- `STATIC_ROOT = BASE_DIR / 'staticfiles'` - Directory where files are collected
- `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'` - Serves static files efficiently
- Whitenoise handles serving CSS, JS, images without extra configuration

### Database
- SQLite3 (`db.sqlite3`) works but data is lost on redeploy
- **Recommended:** Use Render's PostgreSQL database
  - Add PostgreSQL database service in Render
  - Update settings.py with DATABASE_URL
  - Use environment variable: `DATABASE_URL = postgres://...`

### Media Files
- Render's file system is ephemeral (temporary)
- For uploads, use cloud storage (AWS S3, Cloudinary, etc.)
- Or use Render's Disk service for persistent storage

### Security
- Change `SECRET_KEY` to a secure random value
- Keep `DEBUG = false` in production
- Use `SECURE_SSL_REDIRECT = True` (auto via `not DEBUG`)
- Add your domain to `ALLOWED_HOSTS`

## Troubleshooting

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Check STATIC_ROOT path
- Verify Whitenoise middleware is in correct position

### Database Migration Issues
- Render automatically runs migrations (added in build.sh)
- If issues, SSH into service and run: `python manage.py migrate`

### ModuleNotFoundError
- Ensure all imports are in requirements.txt
- Check Python version compatibility

### ALLOWED_HOSTS Error
- Add your Render domain: `your-service.onrender.com`
- Use wildcard if needed: `ALLOWED_HOSTS = ['*']` (already configured)

## Next Steps

1. ✅ Git push all files
2. ✅ Create Render account
3. ✅ Connect repository
4. ✅ Deploy
5. ✅ Test on live URL
6. ✅ (Optional) Set up database and storage services
