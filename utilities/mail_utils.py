import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


def send_email(to_email, username):
    
    subject = f"Welcome to My Store API, {username}!"
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; line-height: 1.6;">
        <h2 style="color: #4CAF50;">Hello, {username}!</h2>
        <p>Thank you for registering at <strong>My Store API</strong>!</p>
        <p>We're excited to have you on board.</p>
    </body>
    </html>
    """
    message = Mail(
        from_email=MAIL_DEFAULT_SENDER,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        return 500