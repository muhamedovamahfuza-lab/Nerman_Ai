# Render.com Environment Setup Guide

## Overview

This guide explains how to configure environment variables for your Django application on Render.com, specifically for the AI chat functionality.

## Required Environment Variables

### 1. AI_API_KEY

**Description**: Your AI service API key (OpenAI or Google Gemini)

**Variable Name**: `AI_API_KEY`

**Format**:
- **For OpenAI**: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - Starts with `sk-proj-` or `sk-`
  - Length: ~50+ characters
  - Get your key from: https://platform.openai.com/api-keys

- **For Google Gemini**: `AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - Starts with `AIzaSy`
  - Length: ~39 characters
  - Get your key from: https://makersuite.google.com/app/apikey

**Example**:
```
AI_API_KEY=AIzaSyDEMO_KEY_xxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 2. AI_API_TYPE

**Description**: Specifies which AI service to use

**Variable Name**: `AI_API_TYPE`

**Allowed Values**: `gemini` or `openai`

**Default**: `gemini`

**Example**:
```
AI_API_TYPE=gemini
```

---

### 3. Other Important Variables

The following variables should also be set in production:

```bash
# Django Secret Key (generate a new one for production)
SECRET_KEY=your-very-long-random-secret-key-here

# Debug mode (ALWAYS set to False in production)
DEBUG=False

# Database URL (automatically set by Render PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Email backend (optional, for password reset emails)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Step-by-Step Setup on Render.com

### Step 1: Navigate to Environment Variables

1. Login to your Render.com dashboard
2. Click on your web service (Django app)
3. Click on the **"Environment"** tab in the left sidebar
4. Scroll to the **"Environment Variables"** section

### Step 2: Add AI_API_KEY

1. Click **"Add Environment Variable"** button
2. In the **Key** field, enter: `AI_API_KEY`
3. In the **Value** field, paste your API key (e.g., `AIzaSyxxxxx...`)
4. Click **"Save Changes"**

> [!IMPORTANT]
> Never share your API key publicly or commit it to Git. Keep it secure in Render's environment variables only.

### Step 3: Add AI_API_TYPE

1. Click **"Add Environment Variable"** again
2. Key: `AI_API_TYPE`
3. Value: `gemini` (or `openai` if using OpenAI)
4. Click **"Save Changes"**

### Step 4: Verify Other Variables

Make sure these are also set:
- `SECRET_KEY` - Should be different from your local `.env`
- `DEBUG` - Should be `False`
- `DATABASE_URL` - Automatically set by Render if you attached PostgreSQL

### Step 5: Deploy

After adding/updating environment variables:

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Wait for deployment to complete (check logs)
3. Your app will restart with new environment variables

---

## Verification

### Check Logs for API Initialization

After deployment, check your Render logs for these messages:

✅ **Success**:
```
AI Service initialized with gemini API (key present)
Gemini AI model configured successfully
```

❌ **Missing API Key**:
```
AI Service initialized but API key is missing! Check environment variable AI_API_KEY
Cannot configure gemini - API key is missing
```

### Test Chat Functionality

1. Navigate to your deployed app: `https://your-app.onrender.com/dashboard/ai-tasks/`
2. Create a new chat
3. Send a test message
4. You should receive an AI response

---

## Troubleshooting

### Issue 1: "API kalit topilmadi" Error

**Symptoms**: Chat returns error message about missing API key

**Solution**:
1. Verify `AI_API_KEY` is set in Render environment variables
2. Check for typos in the variable name (case-sensitive)
3. Redeploy after adding the variable
4. Check logs for initialization messages

### Issue 2: Authentication Error

**Symptoms**: "Autentifikatsiya xatosi" or "API kaliti noto'g'ri"

**Solution**:
1. Verify API key is valid and active
2. For OpenAI: Check billing and quota at https://platform.openai.com/usage
3. For Gemini: Verify key at https://makersuite.google.com/app/apikey
4. Regenerate the API key if necessary
5. Update the key in Render and redeploy

### Issue 3: Rate Limit Errors

**Symptoms**: "So'rovlar soni limitdan oshdi"

**Solution**:
1. Wait a few minutes before trying again
2. For OpenAI: Upgrade your plan or add credits
3. For Gemini: Check quota limits in Google Cloud Console

### Issue 4: CSRF Token Errors

**Symptoms**: 403 Forbidden errors when sending messages

**Solution**:
1. Add your Render URL to `CSRF_TRUSTED_ORIGINS` in `settings.py`:
   ```python
   CSRF_TRUSTED_ORIGINS = [
       'https://your-app.onrender.com',
   ]
   ```
2. Clear browser cookies and try again
3. Check browser console for JavaScript errors

### Issue 5: Environment Variables Not Loading

**Symptoms**: Variables show as `None` in logs

**Solution**:
1. Ensure you clicked "Save Changes" after adding variables
2. Trigger a manual deploy to reload environment
3. Check variable names match exactly (no spaces, correct case)
4. View logs immediately after deploy to see initialization

---

## Security Best Practices

### ✅ Do:
- Store API keys only in Render environment variables
- Use different `SECRET_KEY` for production vs development
- Set `DEBUG=False` in production
- Regularly rotate API keys
- Monitor API usage and costs

### ❌ Don't:
- Commit API keys to Git
- Share API keys in screenshots or logs
- Use the same API key across multiple projects
- Leave `DEBUG=True` in production
- Expose your `.env` file publicly

---

## Cost Management

### Google Gemini
- Free tier: 60 requests per minute
- View quota: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas

### OpenAI
- Pay-as-you-go pricing
- Set usage limits in: https://platform.openai.com/account/limits
- Monitor costs: https://platform.openai.com/usage

---

## Getting API Keys

### Google Gemini (Recommended for Free Tier)
1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Select or create a Google Cloud project
4. Copy the generated key (starts with `AIzaSy`)

### OpenAI
1. Go to: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Give it a name (e.g., "Render Production")
4. Copy the key (starts with `sk-`)
5. Add payment method at: https://platform.openai.com/account/billing

---

## Quick Reference

| Variable | Required | Example Value | Where to Get |
|----------|----------|---------------|--------------|
| `AI_API_KEY` | **Yes** | `AIzaSy...` | [Gemini](https://makersuite.google.com/app/apikey) or [OpenAI](https://platform.openai.com/api-keys) |
| `AI_API_TYPE` | **Yes** | `gemini` | Choose: `gemini` or `openai` |
| `SECRET_KEY` | **Yes** | `django-insecure-...` | Generate with Django |
| `DEBUG` | **Yes** | `False` | Must be `False` in production |
| `DATABASE_URL` | Auto | `postgresql://...` | Auto-set by Render |

---

## Need Help?

- **Django Logs**: Click "Logs" tab in Render dashboard
- **AI Service Logs**: Search for "AI Service" in logs
- **Error Details**: Check browser Console (F12) → Network tab
- **API Status**: Check provider's status page

For more information:
- [Render Environment Variables Docs](https://render.com/docs/environment-variables)
- [Django Settings Best Practices](https://docs.djangoproject.com/en/stable/topics/settings/)
