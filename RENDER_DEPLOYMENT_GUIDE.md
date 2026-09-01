# 🚀 Deploying Django REST Backend on Render.com (100% Free - No Credit Card)

This guide walks you through deploying your **Inspire 2026 Django REST Backend** to **[Render.com](https://render.com/)** in 3 simple steps.

---

## 📋 Overview
- **Hosting Cost**: **100% Free** (Free Web Service Tier)
- **Credit Card Required?**: ❌ **No credit card required** (Sign in with your GitHub account)
- **Public Backend URL**: `https://inspire-backend-xxxx.onrender.com/api/`

---

## 🛠️ Step 1: Push Your Latest Code to GitHub

Open PowerShell in your project folder and run:

```bash
cd c:\Users\user\Desktop\Inspire--main
git add .
git commit -m "Configure Django backend for Render deployment"
git push -u origin main --force
```

---

## 🌐 Step 2: Deploy on Render.com

1. Go to **[https://render.com](https://render.com)**.
2. Click **GET STARTED FOR FREE** (or **Sign In**) -> Click **Continue with GitHub**.
3. In your Render Dashboard, click the blue **+ New** button (top right) -> Select **Web Service**.
4. Click **Build and deploy from a Git repository** -> Click **Next**.
5. Connect your GitHub repository: select **`Poornaaaaa/inspire`** and click **Connect**.
6. Fill in the following fields:

| Field | Value to Enter / Select |
| :--- | :--- |
| **Name** | `inspire-backend` *(or any name you like)* |
| **Language / Runtime** | `Python 3` |
| **Region** | `Singapore (Southeast Asia)` or `Frankfurt` or `Oregon` |
| **Branch** | `main` |
| **Root Directory** | `inspire_backend` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn inspire_project.wsgi:application` |
| **Instance Type** | Select **Free ($0/month)** |

7. Click **Create Web Service** at the bottom of the page!

*(Render will now run `./build.sh`, apply your database migrations, seed all 11 squads and 14 events, and launch Gunicorn automatically in about 1–2 minutes).*

---

## 🔗 Step 3: Connect Your Live Render URL to Your Website

Once Render finishes deploying, it will give you a public URL (e.g. `https://inspire-backend-xxxx.onrender.com`).

1. Open [`index.html`](file:///c:/Users/user/Desktop/Inspire--main/index.html) and update line ~8603:
   ```javascript
   const DJANGO_API_BASE_URL = "https://inspire-backend-xxxx.onrender.com/api";
   ```
2. Open [`admin.html`](file:///c:/Users/user/Desktop/Inspire--main/admin.html) and update line ~2157:
   ```javascript
   const DJANGO_API_BASE_URL = "https://inspire-backend-xxxx.onrender.com/api";
   ```
3. Push the updated HTML files to GitHub:
   ```bash
   git add index.html admin.html
   git commit -m "Connected live Render backend API URL"
   git push -u origin main
   ```

🎉 **Your entire Inspire 2026 Fest Backend is now live 24/7 on Render!**
