
# Email-Open-Tracker-Render

Email-Open-Tracker is a **Flask-based app** for tracking when recipients open emails via a **1×1 transparent pixel**.  
It logs each open event (timestamp, IP, location, user agent) into a CSV file and provides endpoints to **view logs (JSON)** or **download them (CSV)**.  
Easily deployable on **Render** with minimal setup.

---

## Project Overview
This repo includes two main scripts:
- **`send_mail.py`** – Sends emails via Gmail SMTP with a tracking pixel embedded.
- **`app.py`** – Flask backend that serves the tracking pixel and logs opens.

---

## Why Use Render?
- **Fast Flask Deployment** – No manual server setup; SSL included.
- **Public URL for Tracking** – Emails need a publicly accessible pixel.
- **Free Tier** – Sufficient for prototypes and small-scale use.
- **GitHub Auto-Deploy** – Push changes, and Render redeploys automatically.
- **Managed Scaling** – Handles uptime and traffic automatically.

---

## Step 1: Configure Gmail App Password for SMTP
1. **Enable 2-Step Verification**  
   - Go to your Google Account → **Security** → Turn on 2FA.

2. **Create App Password**  
   - Go to **App Passwords** (visible only with 2FA enabled).  
   - Select **Mail**, choose your device, or use "Other" and name it (e.g., "Email Tracker").  
   - Generate a 16-character password (e.g., `abcd efgh ijkl mnop`).

3. **Use It in the Script**  
   In `send_mail.py`:
   ````python
   EMAIL_ADDRESS = "your-email@gmail.com"
   EMAIL_PASSWORD = "abcd efgh ijkl mnop"
````

4. **(Optional) Use Environment Variables**
   For security:

   ```bash
   export EMAIL_PASSWORD="abcd efgh ijkl mnop"
   ```

   And in the script:

   ```python
   import os
   EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
   ```

---

## Step 2: Deploy Flask App on Render

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<your-username>/Email-Open-Tracker-Render.git
   cd Email-Open-Tracker-Render
   ```

2. **Sign Up for Render**
   Create a free account at [Render](https://render.com).

3. **Deploy**

   * Click **New → Web Service**.
   * Connect your GitHub repo and branch.
   * Choose **Python 3** as the runtime.
   * Set the **Start Command**:

     ```bash
     gunicorn app:app
     ```
   * Render auto-installs from `requirements.txt`.

4. **Get Tracking URL**
   Once live, Render provides:

   ```
   https://your-app-name.onrender.com
   ```

   Use this as `TRACKING_BASE_URL` in `send_mail.py`.

---

## Step 3: Sending and Tracking Emails

1. Update `send_mail.py`:

   ```python
   TRACKING_BASE_URL = "https://your-app-name.onrender.com"
   EMAIL_ADDRESS = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-app-password"
   ```

2. Send a tracked email:

   ```bash
   python send_mail.py
   ```

3. When the recipient opens the email (with images enabled), the backend logs the event automatically.

---

## Step 4: Viewing Logs

* **View logs for a specific email ID**:

  ```
  https://your-app-name.onrender.com/view_logs/<email_id>
  ```
* **Download all logs (CSV with header)**:

  ```
  https://your-app-name.onrender.com/download_logs
  ```

---

## Files in This Repo

* `app.py` – Flask backend for tracking pixel and logs (runs on Render).
* `send_mail.py` – Sends emails with tracking pixels.
* `transparent.png` – 1×1 pixel image served by the backend.
* `requirements.txt` – Python dependencies.
* `README.md` – This guide.

---

## Example Workflow

1. Deploy the backend on Render.
2. Update `send_mail.py` with your Render URL and Gmail App Password.
3. Send a tracked email.
4. Logs (IP, location, timestamp, user agent) are saved automatically.
5. View or download logs anytime.

---

