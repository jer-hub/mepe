# Django Backend Deployment to Vercel

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed: `npm i -g vercel`
3. A database (PostgreSQL recommended for production)

## Deployment Steps

### 1. Prepare Your Environment Variables

Create a `.env` file based on `.env.example` and configure your environment variables:

```bash
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,your-domain.vercel.app
DATABASE_URL=postgresql://username:password@hostname:port/database_name
```

### 2. Database Setup

For production, you'll need a PostgreSQL database. Some recommended options:

- **Neon** (https://neon.tech) - Free PostgreSQL with generous limits
- **Supabase** (https://supabase.com) - Free tier with PostgreSQL
- **Railway** (https://railway.app) - Simple PostgreSQL hosting
- **PlanetScale** (https://planetscale.com) - MySQL alternative

Get your database URL and add it to your environment variables.

### 3. Deploy to Vercel

#### Option A: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from your project directory:
   ```bash
   vercel
   ```

4. Follow the prompts and add your environment variables when asked.

#### Option B: Using Vercel Dashboard

1. Push your code to GitHub
2. Go to https://vercel.com/dashboard
3. Click "New Project"
4. Import your GitHub repository
5. Configure environment variables in the project settings
6. Deploy

### 4. Configure Environment Variables in Vercel

In your Vercel dashboard, go to your project settings and add these environment variables:

- `DEBUG` = `False`
- `SECRET_KEY` = Your secure secret key
- `ALLOWED_HOSTS` = `localhost,127.0.0.1,.vercel.app,your-domain.vercel.app`
- `DATABASE_URL` = Your database connection string

### 5. Run Migrations

After deployment, you'll need to run migrations. You can do this by:

1. Connecting to your database directly and running migrations
2. Or using a management command if your hosting provider supports it

## Project Structure

```
backend/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── web/
│   └── (your Django app)
├── static/
├── requirements.txt
├── vercel.json
├── build_files.sh
├── runtime.txt
└── manage.py
```

## Important Files for Vercel

- `vercel.json` - Vercel configuration
- `build_files.sh` - Build script for static files
- `runtime.txt` - Python version specification
- `requirements.txt` - Python dependencies

## Troubleshooting

### Common Issues:

1. **Static files not loading**: Make sure `STATIC_ROOT` is set correctly and `collectstatic` runs during build.

2. **Database connection errors**: Verify your `DATABASE_URL` is correct and the database is accessible.

3. **Import errors**: Ensure all dependencies are in `requirements.txt`.

4. **CORS issues**: If you have a frontend, you may need to configure CORS settings.

### Vercel Logs

Check your deployment logs in the Vercel dashboard for any build or runtime errors.

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,.vercel.app` |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host/db` |

## Next Steps

1. Set up your database and run migrations
2. Configure your domain (if using custom domain)
3. Set up monitoring and logging
4. Configure CORS if you have a frontend application
