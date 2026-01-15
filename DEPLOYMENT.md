# Deploying NERMAN.AI to Render.com

This guide will walk you through deploying your Django application to Render.com.

## Prerequisites

- GitHub repository with your code
- Render.com account (free tier works)
- Your application runs locally without errors

## Step 1: Push Code to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `nerman-ai` (or your preferred name)
   - **Region**: Select closest to your users
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn nerman_ai.wsgi:application`
   - **Plan**: Free (or paid if needed)

## Step 3: Configure Environment Variables

In Render dashboard, go to **Environment** tab and add:

### Required Variables
```
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
AI_API_KEY=<your-gemini-api-key>
AI_API_TYPE=gemini
```

### Optional Variables
```
LANGUAGE_CODE=ru-ru
TIME_ZONE=Asia/Tashkent
```

> **Note**: Render automatically provides `DATABASE_URL` for PostgreSQL

## Step 4: Add PostgreSQL Database

1. In your Render service, click **"New +"** → **"PostgreSQL"**
2. Name it (e.g., `nerman-ai-db`)
3. Select Free tier
4. Create database
5. Render will automatically set `DATABASE_URL` environment variable

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies
   - Collect static files
   - Run migrations
   - Start Gunicorn server

3. Monitor the build logs for any errors

## Step 6: Create Superuser

After successful deployment, use Render Shell:

1. Go to your service → **Shell** tab
2. Run:
```bash
python manage.py createsuperuser
```

## Step 7: Verify Deployment

Your application will be available at:
```
https://your-service-name.onrender.com
```

Test the following:
- ✅ Homepage loads
- ✅ Static files (CSS, images) load correctly
- ✅ Login/Register pages work
- ✅ Admin panel accessible at `/admin/`

## Troubleshooting

### Static Files Not Loading
- Check `STATICFILES_STORAGE` setting
- Verify `./build.sh` runs `collectstatic`
- Check Render logs for errors

### Database Connection Issues
- Verify `DATABASE_URL` is set automatically
- Check database is created and running
- Review migration logs

### Application Won't Start
- Check `gunicorn` is in `requirements.txt`
- Verify start command: `gunicorn nerman_ai.wsgi:application`
- Review build logs for Python errors

## Important Notes

⚠️ **Security**:
- Never commit `.env` to GitHub
- Always use `DEBUG=False` in production
- Use strong `SECRET_KEY`

📝 **Free Tier Limitations**:
- Service spins down after 15 minutes of inactivity
- First request may take 30-60 seconds (cold start)
- 750 hours/month free

## Updating Your Deployment

When you push changes to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically rebuild and redeploy.

## Useful Commands

Generate a new SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Check deployment settings:
```bash
python manage.py check --deploy
```

---

🎉 **Your NERMAN.AI application is now live on Render!**
