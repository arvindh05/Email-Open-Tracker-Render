import smtplib  # Library to send emails using the Simple Mail Transfer Protocol (SMTP)
import time  # Used to generate a unique cache-busting parameter for the tracking pixel
from email.mime.text import MIMEText  # For creating plain text email content
from email.mime.multipart import MIMEMultipart  # For combining plain text and HTML email parts


# Gmail SMTP server details (used for sending emails)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Your Gmail credentials
EMAIL_ADDRESS = "hello@gmail.com" # Use your email id here
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  # Use App Password for Gmail

# Change this to your deployed app URL after deployment!
TRACKING_BASE_URL = "https://email-tracker-backend-id8y.onrender.com"

def send_mail(recipient_mail, subject, body, email_id="track001"):
        """
    Sends an email with a hidden 1×1 tracking pixel to monitor when the recipient opens the email.
    Logs are captured by the Flask app running on Render.
    """
    try:
        # Creating a cache-buster to prevent email clients from caching the tracking pixel

        cache_buster = int(time.time())
        # HTML email body with the tracking pixel embedded
        # The pixel is invisible (1x1, display:none)
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

# Test email when running this script directly
if __name__ == "__main__":
    recipient = "arvindh9701@gmail.com"
    subject = "Tracked Email - Production"
    body = "Hello! This is a tracked email. Please open it with images enabled."
    send_mail(recipient, subject, body, email_id="packaroo001")
