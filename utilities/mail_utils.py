import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


def send_email(to_email, username):
    message = Mail(
        from_email=MAIL_DEFAULT_SENDER,
        to_emails=to_email,
        subject=f"Hello {username},",
        html_content=f"""
        <h1>Hello {username},</h1>
        <p>Welcome to our services!</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        return 500