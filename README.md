# HR Manager

An HR checklist web app built with Django. It keeps employee records, tracks passport and BRP (Biometric Residence Permit) expiry dates, warns HR about documents that expire soon, emails reminders automatically, and generates offer letters as PDFs.

## Features

- **Staff login** using Django's built-in authentication.
- **Employee records**: name, date of birth, email, position, salary, phone number, plus uploaded passport and BRP documents.
- **Expiry alerts**: every page shows passports and BRPs that expire within the next 60 days.
- **Offer letters**: fills an employee's details into a PDF template (`templates/Offerletter.pdf`) with PyMuPDF and downloads it.
- **Employee directory**: view, edit and delete employees in place (AJAX).
- **Duplicate check**: warns live if an email address is already registered.
- **Email everyone**: send one message to all employees from the app.
- **Scheduled emails** (Celery + Redis): a daily reminder to employees whose documents expire within 60 days.

## Tech stack

| Part | Used |
|---|---|
| Backend | Python, Django 5.0 |
| Database | SQLite |
| PDFs | PyMuPDF (`fitz`) |
| Background jobs | Celery 5, Celery Beat, Redis |
| Frontend | Django templates, Bootstrap (SB Admin 2 theme), jQuery |

## Project structure

```
HRchecklist/      Django project: settings, URLs, Celery app and schedule
HRoperations/     Main app: models, views, forms, Celery tasks, migrations
templates/        HTML pages and the offer letter PDF template
static/           CSS, JavaScript and vendor libraries
manage.py
requirements.txt
```

## Getting started

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000 and sign in with the user you created.

### Email and secrets

Credentials are read from environment variables, never stored in the code:

```bash
export DJANGO_SECRET_KEY="any-long-random-string"
export EMAIL_HOST_USER="you@gmail.com"
export EMAIL_HOST_PASSWORD="your-gmail-app-password"
export DEFAULT_FROM_EMAIL="you@gmail.com"   # optional, defaults to EMAIL_HOST_USER
```

`db.sqlite3`, uploaded files in `documents/` and generated offer letters are created locally and are not part of the repository.

### Scheduled emails (optional)

Requires a running Redis server on `localhost:6379`.

```bash
celery -A HRchecklist worker -l info
celery -A HRchecklist beat -l info
```

## Main pages

| URL | Page |
|---|---|
| `/` | Login |
| `/add_employee/` | Dashboard with expiry alerts and the add-employee form |
| `/employees/` | Employee directory (edit / delete) |
| `/send_email/` | Email all employees |
| `/generate_filled_pdf/<id>/` | Download an employee's offer letter |
| `/admin/` | Django admin |

## Known issues

- `generate_filled_pdf` uses a hard-coded path to the offer letter template, and `views.py` uses `os.path` without importing `os`. Import `os` and use a path relative to the project (for example `BASE_DIR / "templates" / "Offerletter.pdf"`).
- The Celery schedule also runs `send_email_to_even_numbered_employees` **every 10 seconds**, emailing every employee whose first name starts with "M". This looks like a test task. Remove it from `HRchecklist/celery.py` before running Celery Beat with real data.
- `DEBUG = True` is set in `settings.py`. Turn it off before deploying.
