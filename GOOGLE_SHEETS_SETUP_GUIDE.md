# 📊 INSPIRE 2026 — Google Cloud Real-Time Leaderboard & Pass Email Setup Guide

Follow this quick **2-minute setup** to enable **real-time live scoring synchronization** between Admin Console (`admin.html`), Public Website (`index.html`), and **Google Sheets**, plus automatic **Digital Delegate Pass email dispatch** to registered students!

---

### 🔹 Step 1: Open Your Google Spreadsheet
1. Open your existing spreadsheet (e.g. **`Inspire 2026 Database`**) or create a new one at [https://sheets.new](https://sheets.new).

---

### 🔹 Step 2: Open Apps Script Editor
1. In the Google Sheet top menu bar, click: **Extensions** ➔ **Apps Script**.
2. A new code editor window will open.
3. Delete any default code inside `Code.gs`.

---

### 🔹 Step 3: Paste the Full Backend Script
1. Open the file [`google_sheets_sync_script.gs`](google_sheets_sync_script.gs) in this project folder.
2. Copy its entire content and **paste it into the Apps Script `Code.gs` editor**.
3. Click the **💾 Save** icon (or press `Ctrl + S`).

---

### 🔹 Step 4 (OPTIONAL BUT RECOMMENDED): Authorize Permissions & Test in 1 Click!
1. In the top toolbar of Apps Script, find the function dropdown (where it says `doPost` or `myFunction`).
2. Select **`testSendEmail`** from the dropdown.
3. Click the **▶️ Run** button.
4. When prompted:
   - Click **Review permissions** ➔ Choose your Google Account.
   - Click **Advanced** (bottom left of modal) ➔ Click **Go to Inspire 2026 (unsafe)** ➔ Click **Allow**.
5. Check your personal Gmail inbox — you will immediately receive an official Inspire 2026 test pass!

---

### 🔹 Step 5: Deploy as Web App
1. In the top-right corner of the Apps Script window, click the blue **Deploy** button.
   - **If updating an existing deployment**:
     - Click **Manage deployments** ➔ Click the **✏️ Edit (pencil)** icon on your active deployment ➔ Under *Version*, select **New version** ➔ Click **Deploy**.
   - **If deploying for the first time**:
     - Click **New deployment** ➔ Click the ⚙️ **gear icon** next to "Select type" and choose **Web app**.
     - Set **Description**: `Inspire 2026 Live Leaderboard & Registrations Sync`
     - Set **Execute as**: `Me (your_email@gmail.com)` *(⚠️ Ensures pass emails are sent from your email)*
     - Set **Who has access**: **`Anyone`** *(⚠️ IMPORTANT: Choose "Anyone" so all student phones & devices can sync scores and submit registrations).*
     - Click **Deploy**.
2. Copy the **Web App URL** shown in the confirmation window (e.g. `https://script.google.com/macros/s/AKfycb.../exec`).

---

### 🔹 Step 6: Verify Web App URL in Code
Both [`index.html`](index.html) and [`admin.html`](admin.html) contain `GOOGLE_SHEETS_WEB_APP_URL`. If your newly deployed URL is different, paste it inside the quotes:
```javascript
const GOOGLE_SHEETS_WEB_APP_URL = "YOUR_DEPLOYED_WEB_APP_URL";
```

---

## 🏆 How the Live Leaderboard Works:

1. **Clean 0-Point Baseline**: All 11 squads start at **0 PTS**. The public site displays a primed kick-off state.
2. **Instant Admin Point Allocation**: When Admin awards points in `admin.html` (via quick buttons, custom score editor, bulk allocator, or 14-track matrix scorer):
   - Local tabs / windows update in **0 milliseconds** via `BroadcastChannel`.
   - Google Cloud is updated automatically in the background.
3. **Cross-Device Spectator Sync**: Mobile phones, projector screens, and laptops viewing `index.html` sync every 5 seconds and instantly upon switching tabs.
4. **Dynamic Podium Activation**: The Gold (#1 Center), Silver (#2 Left), and Bronze (#3 Right) podium pedestals unlock and animate dynamically as scores are given.
