# Email-Open-Tracker-Render
Email-Open-Tracker is a Flask app for tracking email opens via a 1×1 pixel image. Logs include timestamp, IP, location, and user agent, stored in CSV. Easily deployable on Render, with routes to view logs in JSON or download as CSV.


# Email-Open-Tracker-Render - Setup and Usage Guide
## Overview
This project consists of two main Python scripts:

**1.send_mail.py:** Sends an HTML email embedding a tracking pixel from the deployed backend URL.
**2.app.py:** A Flask backend that serves a tracking pixel image to detect when an email is opened and logs that event (with IP, location, user-agent).

# 1.1: How to Configure Gmail App Password for SMTP

## 1. Enable 2-Step Verification on Your Google Account

- Go to your [Google Account Security page](https://myaccount.google.com/security).
- Under **Signing in to Google**, enable **2-Step Verification** if not already enabled.  
  This step is mandatory for creating an app password.

## 2. Create an App Password

- After enabling 2-Step Verification, return to the Security page.
- Click on **App Passwords** (this option appears only if 2-Step Verification is enabled).
- Select **Mail** as the app, and your device (e.g., choose **Other** and name it "Email Tracker Script").
- Click **Generate**. Google will show a 16-character app password.

## 3. Store the App Password Securely

- Copy the generated app password (e.g., `abcd efgh ijkl mnop`).
- **Do not share this password publicly or commit it to your code repository.**

## 4. Use the App Password in Your Script

Replace the `EMAIL_PASSWORD` variable value in your `send_mail.py` file with this app password:

**python code**
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  # Your generated app password here

## Why Use Render?

- **Easy Deployment:** Quickly deploy Python Flask apps without managing servers.
- **Public URL:** Provides a public HTTPS URL for your tracking pixel to be accessible online.
- **Reliable & Secure:** Handles scaling, uptime, and SSL automatically.
- **GitHub Integration:** Auto-deploy on every Git push for seamless updates.
- **Free Tier:** Generous free plan perfect for prototypes and small projects.
- **Scalable:** Supports databases and background jobs if your project grows.

## 1.2: How to Deploy Your Flask Email Tracker on Render and Get Your Tracking URL

1. **Create a Render Account**  
   - Go to [https://render.com](https://render.com)  
   - Sign up for a free account using GitHub or email.

2. **Prepare Your Code Repository**  
   - Push your project to GitHub.  
   - Ensure it includes:  
     - `app.py` (Flask app)  
     - `requirements.txt` (Python dependencies)  
     - `transparent.png` (tracking pixel image)  
     - Any other necessary files.

3. **Create a New Web Service on Render**  
   - In Render dashboard, click **New → Web Service**.  
   - Connect your GitHub repo and select the branch (e.g., `main`).  
   - Choose environment: **Python 3**.  
   - Set Start Command:  
     ```bash
     python app.py
     ```  
   - Render installs dependencies from `requirements.txt` automatically.

4. **Set Environment Variables (Optional but Recommended)**  
   - Go to your service’s **Settings → Environment**.  
   - Add secrets like email passwords or API keys here to avoid hardcoding.

5. **Deploy**  
   - Click **Create Web Service**.  
   - Monitor build and logs on the Render dashboard.

6. **Get Your Tracking Base URL**  
   - After deployment, you get a URL like:  
     ```
     https://your-app-name.onrender.com
     ```  
   - Use this as the base URL in your email tracker.

7. **Update Your `send_mail.py` Script**  
   - Set `TRACKING_BASE_URL` to your Render URL:  
     ```python
     TRACKING_BASE_URL = "https://your-app-name.onrender.com"
     ```

8. **Send a Test Email**  
   - Run `send_mail.py`.  
   - Open the email in a client that loads images.  
   - Your Flask app will log the email open event.

Here’s the **complete README.md** (ready to put in your GitHub repo) with **all instructions, Gmail App Password setup, why Render is used, and step-by-step usage**:

````markdown
# Email Tracker Backend (Flask + Render)

This project is a **simple email tracking backend** built with Python (Flask) and deployed on **Render**.  
It logs email opens (IP, user agent, timestamp, location) when the recipient loads a tracking pixel embedded in the email.

---

## Why Use Render?
- **Easy Flask Deployment** – No server setup; Render hosts your backend with SSL.
- **Public Tracking URL** – Email clients can access your pixel via a public HTTPS link.
- **Automatic Scaling & Free Tier** – Great for lightweight projects like this.
- **GitHub Integration** – Every push to your repo redeploys your app automatically.

---

## How to Configure Gmail App Password (For Sending Emails)

1. **Enable 2-Step Verification**  
   Go to your Google Account → **Security** → Enable 2-Step Verification.

2. **Create an App Password**  
   - Go to **App Passwords** (only visible after enabling 2FA).  
   - Select **Mail** as the app and choose your device (or "Other", name it).  
   - Generate a 16-character password (e.g., `abcd efgh ijkl mnop`).

3. **Use It Securely**  
   In `send_mail.py`, update:
   ```python
   EMAIL_ADDRESS = "your-email@gmail.com"
   EMAIL_PASSWORD = "abcd efgh ijkl mnop"
````

*(Optional)*: Use environment variables instead:

```bash
export EMAIL_PASSWORD="abcd efgh ijkl mnop"
```

And in your code:

```python
import os
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
```

---

## How to Deploy and Use This Tracker on Render

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create a Render Account

Sign up at [https://render.com](https://render.com) (free tier is enough).

### 3. Deploy the Flask Backend

1. In Render, click **"New" → "Web Service"**.
2. Connect your GitHub repository.
3. Choose **Python 3** as the runtime.
4. Set the **Start Command**:

   ```bash
   gunicorn app:app
   ```
5. Render will install dependencies from `requirements.txt`.
6. Click **Create Web Service** and wait until it goes **Live**.

### 4. Get Your Public Tracking URL

After deployment, Render gives you a URL like:

```
https://your-app-name.onrender.com
```

Use this URL in your email tracking links.

### 5. Update `send_mail.py`

Replace:

```python
TRACKING_BASE_URL = "https://your-app-name.onrender.com"
```

with your Render app URL.

Update:

```python
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
```

### 6. Send a Test Email

Run:

```bash
python send_mail.py
```

The script sends a tracked email with an invisible tracking pixel.

### 7. Check Open Logs

* View logs for a specific email ID:

  ```
  https://your-app-name.onrender.com/view_logs/<email_id>
  ```
* Download all logs (CSV with header):

  ```
  https://your-app-name.onrender.com/download_logs
  ```

Logs include:
`email_id, timestamp, ip, location, user_agent`

---

## Files in This Repo

* **app.py** – Flask backend for tracking pixel and logs (runs on Render).
* **send\_mail.py** – Sends tracked emails using Gmail SMTP.
* **requirements.txt** – Python dependencies.
* **transparent.png** – 1x1 tracking pixel.
* **README.md** – Setup and usage guide.

---

## Example Flow

1. Deploy the backend on Render (get URL).
2. Update `send_mail.py` with your Render URL and Gmail app password.
3. Send tracked emails.
4. Recipients open emails → logs automatically update.
5. View logs in browser or download as CSV.

```

---

Would you like me to also **write the `requirements.txt` (with proper packages)** so the interviewer can deploy without errors?  
Or **create a shorter version (1-page)** for the interviewer? Or **both**?
```

