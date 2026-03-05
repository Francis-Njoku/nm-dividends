# Local Development Setup Guide

## Overview

This Django application has been successfully set up for local development. The server is running on `http://localhost:8000`.

## Prerequisites

- Python 3.14+ (or compatible version)
- pip package manager
- Virtual environment support

## Setup Steps Completed

### 1. Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Dependencies Installed

The following packages have been installed:

- Django 6.0.3
- Django REST Framework 3.16.1
- Django REST Framework SimpleJWT 5.5.1
- Django CORS Headers 4.9.0
- psycopg2-binary 2.9.11
- dj-database-url 3.1.2
- drf-yasg 1.21.15 (Swagger UI)
- django-filter 25.2
- reportlab 4.4.10
- pillow 12.1.1
- pandas 3.0.1
- faker 40.5.1
- weasyprint 68.1
- fpdf2 2.8.7
- chardet 7.0.0
- whitenoise 6.12.0

### 3. Environment Configuration

Created `.env` file with the following variables:

```env
SECRET_KEY=django-insecure-development-key-change-in-production-please
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
SOCIAL_SECRET=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
TWITTER_API_KEY=
TWITTER_CONSUMER_SECRET=
FRONTEND_URL=http://localhost:3000
APP_SCHEME=http
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Database Setup

- Database: SQLite (db.sqlite3)
- All migrations applied successfully
- Superuser created:
  - Username: admin
  - Email: admin@example.com
  - Password: admin123

### 5. Development Server

Server is running on: `http://localhost:8000`

## Available Endpoints

### Main Endpoints

- **Root**: `http://localhost:8000/` - Swagger UI documentation
- **Admin**: `http://localhost:8000/admin/` - Django admin panel
- **Swagger UI**: `http://localhost:8000/` - Interactive API documentation
- **ReDoc**: `http://localhost:8000/redoc/` - Alternative API documentation

### Authentication Endpoints

- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration
- `POST /auth/logout/` - User logout
- `GET /auth/loaduser/` - Load authenticated user
- `POST /auth/email-verify/` - Email verification
- `POST /auth/request-reset-email/` - Password reset request
- `GET /auth/list-users/` - List all users
- `GET /auth/user/<id>/` - Get user details

### Article Endpoints

- `GET /article/posts/` - List all articles
- `POST /article/posts/create/` - Create new article
- `GET /article/posts/<slug>/` - Get article by slug
- `PUT /article/posts/<slug>/update/` - Update article
- `DELETE /article/posts/<slug>/delete/` - Delete article

### Results Endpoints

- `GET /results/` - Results data

### Token Endpoints

- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

## Starting the Development Server

### Start Server

```bash
cd /home/davidaloba/Projects/nm-dividends
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Access the Application

- Open browser and navigate to: `http://localhost:8000`
- For Swagger documentation: `http://localhost:8000/`
- For Django Admin: `http://localhost:8000/admin/` (login with admin/admin123)

## Database Management

### Run Migrations

```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
source venv/bin/activate
python manage.py createsuperuser
```

### Reset Database

```bash
rm db.sqlite3
python manage.py migrate
```

## Development Workflow

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Start Development Server

```bash
python manage.py runserver
```

### 3. Make Code Changes

- Edit files in your codebase
- The server will auto-reload on file changes

### 4. Test Changes

- Access `http://localhost:8000` in your browser
- Use Swagger UI to test API endpoints
- Check Django Admin for database management

## Common Commands

### Check Project Status

```bash
python manage.py check
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Run Tests

```bash
python manage.py test
```

### Open Django Shell

```bash
python manage.py shell
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 0.0.0.0:8001
```

### Import Errors

If you encounter import errors:

```bash
source venv/bin/activate
pip install -r requirements-pip.txt
```

### Database Issues

If you encounter database issues:

```bash
rm db.sqlite3
python manage.py migrate
```

### CORS Issues

If you encounter CORS errors, update the CORS settings in [`dividends/settings.py`](dividends/settings.py:106):

```python
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:3001",
    # Add your frontend URL here
]
```

## Production Deployment Notes

### Security

- Change `SECRET_KEY` in `.env` to a secure, random value
- Set `DEBUG=False` in production
- Use PostgreSQL instead of SQLite
- Configure proper email settings
- Set up SSL/HTTPS
- Configure `ALLOWED_HOSTS` with your production domain

### Environment Variables

Update `.env` with production values:

```env
SECRET_KEY=<your-secret-key>
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-password>
# ... other production settings
```

### Static Files

```bash
python manage.py collectstatic --noinput
```

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django REST Framework SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/
- Swagger UI: Available at `http://localhost:8000/`

## Support

For issues or questions:

1. Check the terminal output for error messages
2. Review Django logs in the terminal
3. Check the `.env` file configuration
4. Ensure all dependencies are installed
5. Verify database migrations are up to date

---

**Server Status**: ✅ Running on http://localhost:8000
**Database**: ✅ SQLite (db.sqlite3) - All migrations applied
**Superuser**: ✅ Created (admin/admin123)
**Dependencies**: ✅ All required packages installed
