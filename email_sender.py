import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import dotenv

from constants import (EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER,
                       TO_EMAIL)
from utils.env_handler import get_env_var

dotenv.load_dotenv()


def send_email(to_email, subject, body=None, file_path=None, text_file=None):
    """Send an email to the specified email address."""
    msg = MIMEMultipart()
    msg["From"] = get_env_var(EMAIL_ADDRESS)
    msg["To"] = to_email
    msg["Subject"] = subject

    # If text_file is not None, read it and append to body
    if text_file is not None:
        with open(text_file, "r") as f:
            body = f"<pre>{f.read()}</pre>"

    # Attach the body with the msg instance
    if body is not None:
        msg.attach(MIMEText(body, "html"))  # Set the MIME type to "html"

    if file_path is not None:
        # Open the file in binary
        binary = open(file_path, "rb")

        payload = MIMEBase(
            "application", "octet-stream", Name=os.path.basename(file_path)
        )
        # To change the payload into encoded form
        payload.set_payload((binary).read())
        encoders.encode_base64(payload)

        # Add payload header with pdf name
        payload.add_header(
            "Content-Decomposition", "attachment", filename=os.path.basename(file_path)
        )
        msg.attach(payload)

    try:
        with smtplib.SMTP(
            get_env_var(SMTP_SERVER), int(get_env_var(SMTP_PORT))
        ) as server:
            server.starttls()
            server.login(get_env_var(EMAIL_ADDRESS), get_env_var(EMAIL_PASSWORD))
            server.sendmail(get_env_var(EMAIL_ADDRESS), to_email, msg.as_string())
    except (
        smtplib.SMTPException,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPServerDisconnected,
        smtplib.SMTPConnectError,
    ) as e:
        logging.error(f"Failed to send email: {str(e)}")
