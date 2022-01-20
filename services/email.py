import os

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

app_path = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.expanduser(app_path)
load_dotenv(os.path.join(project_folder, '.env'))  # load the content of the .env as environment var

email_conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM=os.environ.get('MAIL_FROM'),
    MAIL_PORT=os.environ.get('MAIL_PORT'),
    MAIL_SERVER=os.environ.get('MAIL_SERVER'),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


async def send_email_async(subject: str, email_to: str, body, email_conf: ConnectionConfig = email_conf):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=str(body)
    )

    fm = FastMail(email_conf)

    await fm.send_message(message, template_name='email.html')
