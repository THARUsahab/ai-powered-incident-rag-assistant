
import os
import ssl
import smtplib
import requests

from email.message import EmailMessage
from dotenv import load_dotenv

# Read configuration from .env
load_dotenv(override=True)


# ---------------------------------------
# 1. Slack Notification
# ---------------------------------------
def send_slack_alert(message):

    webhook = os.getenv("SLACK_WEBHOOK_URL", "").strip()

    if not webhook:
        print("Slack not configured")
        return

    try:
        response = requests.post(
            webhook,
            json={"text": message},
            timeout=10
        )

        response.raise_for_status()
        print("Slack alert sent successfully!")

    except requests.RequestException as error:
        print(f"Slack notification failed: {error}")


# ---------------------------------------
# 2. Gmail Email Notification
# ---------------------------------------
def send_email_alert(subject, message):

    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "465"))

    username = os.getenv("SMTP_USERNAME", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
    recipient = os.getenv("ALERT_EMAIL", "").strip()

    if not all([host, username, password, recipient]):
        print("Email not configured")
        return

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = username
    email["To"] = recipient
    email.set_content(message)

    try:
        print("Connecting to Gmail SMTP SSL...")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            host,
            port,
            timeout=20,
            context=ssl.create_default_context()
        ) as smtp:

            print("Secure SMTP connection established")

            smtp.login(username, password)
            print("Gmail authentication successful")

            smtp.send_message(email)
            print("Email alert sent successfully!")

    except smtplib.SMTPAuthenticationError as error:
        print(
            f"Gmail authentication failed. "
            f"SMTP code: {error.smtp_code}"
        )

    except smtplib.SMTPServerDisconnected:
        print("Gmail disconnected during SMTP communication")

    except (smtplib.SMTPException, OSError) as error:
        print(
            f"Email notification failed: "
            f"{type(error).__name__}: {error}"
        )


# ---------------------------------------
# 3. Main Incident Notification
# ---------------------------------------
def notify_incident(url, error, details):

    message = (
        f"WEBSITE INCIDENT\n"
        f"-------------------------\n"
        f"Website: {url}\n"
        f"Error: {error}\n"
        f"Details: {details}\n"
        f"-------------------------\n"
        f"Please investigate this incident."
    )

    # Console alert
    print("\n" + message)

    # Slack alert
    send_slack_alert(message)

    # Email alert
    send_email_alert(
        subject=f"Website Incident Alert: {error}",
        message=message
    )
