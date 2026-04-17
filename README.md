# MEPE Member Portal (Django)

A Django-based member portal for **MEPE Multipurpose Cooperative**.  
Members can enter their chapa/member ID to view account particulars, then filter and search transaction records.

## Features

- Member lookup using chapa ID
- Account particulars view with:
  - filter by S/L (particular)
  - search by reference number
- Responsive UI templates (Tailwind via CDN)
- Static file handling with WhiteNoise
- Deployment configuration for Vercel
- Data transfer management command from MySQL to PostgreSQL

## Tech Stack

- Python
- Django
- PostgreSQL (default database)
- MySQL (secondary database alias for data transfer)
- WhiteNoise + Gunicorn

## Repository Structure

```text
.
├── backend/                  # Django project settings and URL config
├── web/                      # Main Django app (models, views, templates, commands)
├── static/                   # Project static assets
├── staticfiles_build/        # Built static output used in deployment
├── manage.py
├── pyproject.toml
├── requirements.txt
├── vercel.json
└── DEPLOYMENT.md
```

## Prerequisites

- Python 3.13 is declared in `.python-version` / `pyproject.toml`  
  (Vercel runtime is configured separately in `runtime.txt` / `vercel.json`)
- pip
- PostgreSQL (for `default` DB)
- MySQL (if using transfer features with `mysql` DB alias)

## Local Setup

1. **Clone and enter the project**
   ```bash
   git clone https://github.com/jer-hub/mepe.git
   cd mepe
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root with values like:
   ```bash
   DEBUG=True
   # Local/dev only. Use a long random value in production.
   SECRET_KEY=dev-only-change-this-to-a-long-random-secret
   ALLOWED_HOSTS=localhost,127.0.0.1
   POSTGRES_DB=mepecoop_web
   POSTGRES_USER=postgres
   # Local/dev only.
   POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   DB_NAME=mepecoop_web
   DB_USER=root
   # Local/dev only.
   DB_PASSWORD=CHANGE_ME_MYSQL_PASSWORD
   DB_HOST=localhost
   DB_PORT=3306
   # Optional: if set, Django parses this as the default DB URL
   # DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. Open: `http://127.0.0.1:8000/`

## Useful Commands

- Django system check:
  ```bash
  python manage.py check
  ```

- Run tests:
  ```bash
  python manage.py test
  ```

- Collect static files:
  ```bash
  python manage.py collectstatic --noinput --clear
  ```

- Transfer data from MySQL to PostgreSQL:
  ```bash
  python manage.py transfer_data
  ```

- Optimize static assets:
  ```bash
  python manage.py optimize_static --help
  ```

## Deployment

- Vercel configuration: `vercel.json`
- Build script: `build_files.sh`
- Detailed guide: `DEPLOYMENT.md`

## Notes

- The project defines both `default` and `mysql` database connections in `backend/settings.py`.
- Tests can require all configured DB backends to be available depending on environment and installed DB drivers.
