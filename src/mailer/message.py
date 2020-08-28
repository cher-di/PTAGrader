import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Message:
    def __init__(self, body: str, subject: str = None):
        self._message = MIMEMultipart('alternative')
        self._message.attach(MIMEText(body, 'html'))
        if subject:
            self._message['Subject'] = subject

    def attach(self, filepath: str, filename: str = None):
        with open(filepath, 'rb') as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
        self._message.attach(part)
        encoders.encode_base64(part)
        if not filename:
            filename = os.path.basename(filepath)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    @property
    def message(self) -> MIMEMultipart:
        return self._message
