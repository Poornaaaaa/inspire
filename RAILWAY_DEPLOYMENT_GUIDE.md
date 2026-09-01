# 🚂 Railway.app Cloud Deployment Guide for Inspire 2026

This guide walks you through deploying your **Django REST API Backend** to **Railway.app** in under 3 minutes.

---

## 🛠️ Prerequisites Already Completed For You

All necessary configuration files have been prepared:
- ✅ `inspire_backend/requirements.txt` (includes `gunicorn`, `whitenoise`, `django-cors-headers`, `djangorestframework`)
- ✅ `inspire_backend/Procfile` (auto-runs migrations, seeds data, and starts Gunicorn)
- ✅ `inspire_backend/railway.json` & `nixpacks.toml` (Nixpacks build specifications)
- ✅ `inspire_backend/inspire_project/settings.py` (CORS headers, CSRF trusted origins, and WhiteNoise static asset serving)

---

## 🚀 Method 1: Deploy via Railway Web Dashboard (Easiest - 3 Steps)

### Step 1: Push Your Code to GitHub
1. Open a terminal in your project directory:
   ```bash
   git add .
   git commit -m "Configure Django REST backend for Railway deployment"
   git push origin main
   ```

### Step 2: Connect GitHub Repository to Railway
1. Go to **[Railway.app](https://railway.app/)** and log in with your GitHub account.
2. Click **+ New Project** -> Select **Deploy from GitHub repo**.
3. Select your repository (`Inspire--main`).
4. Click **Deploy Now**.
   *(Railway will automatically detect `railway.json` and build the Django application)*.

### Step 3: Generate Public Domain
1. In your Railway project dashboard, click on your service card.
2. Navigate to **Settings** -> Scroll down to **Networking**.
3. Click **Generate Domain** (e.g. `https://inspire-production-xxxx.up.railway.app`).

---

## ⚡ Method 2: Deploy directly via Railway CLI (No Git push needed)

If you have Node.js / npm installed, you can deploy directly from your local terminal:

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```
2. Log in:
   ```bash
   railway login
   ```
3. Initialize and deploy:
   ```bash
   cd inspire_backend
   railway init
   railway up
   ```
4. Generate domain:
   ```bash
   railway domain
   ```

---

## 🔗 Step 4: Connect the Deployed Railway URL to Your Website

Once Railway gives you your live domain URL (e.g., `https://inspire-production-xxxx.up.railway.app`):

1. Open [`index.html`](file:///c:/Users/user/Desktop/Inspire--main/index.html) and update line ~8603:
   ```javascript
   const DJANGO_API_BASE_URL = "https://inspire-production-xxxx.up.railway.app/api";
   ```
2. Open [`admin.html`](file:///c:/Users/user/Desktop/Inspire--main/admin.html) and update line ~2157:
   ```javascript
   const DJANGO_API_BASE_URL = "https://inspire-production-xxxx.up.railway.app/api";
   ```

🎉 **Your entire Inspire 2026 fest system is now live on the internet 24/7!**
