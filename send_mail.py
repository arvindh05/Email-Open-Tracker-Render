import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "arvindh0501@gmail.com" # Use your email id here
EMAIL_PASSWORD = "uzvd afcm kssx egli"  # Use App Password for Gmail

# Change this to your deployed app URL after deployment!
TRACKING_BASE_URL = "https://email-tracker-backend-id8y.onrender.com"

def send_mail(recipient_mail, subject, body, email_id="track001"):
    try:
        cache_buster = int(time.time())
        html_body = f"""
        <html>
            <body>
                <p>{body}</p>
                <img src="{TRACKING_BASE_URL}/track/{email_id}.png?cb={cache_buster}" width="1" height="1" style="display:none;">
            </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_mail
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_mail, msg.as_string())

        print(f"[SENT] Email sent to {recipient_mail} (Tracking ID: {email_id})")
    except Exception as e:
        print(f"[ERROR] Sending email failed: {e}")

if __name__ == "__main__":
    recipient = "arvindh9701@gmail.com"
    subject = "Tracked Email - Production"
    body = "Hello! This is a tracked email. Please open it with images enabled."
    send_mail(recipient, subject, body, email_id="packaroo001")
