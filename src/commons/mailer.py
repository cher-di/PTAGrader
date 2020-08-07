import smtplib as _smtplib
import typing as _typing

from email.message import EmailMessage
from email.header import Header
from email.utils import formataddr


class Mailer:
    def __init__(self, mail_server: str):
        self._mail_server = mail_server
        self._port = 465

    def send(self, from_addr: str, to_addr: str or _typing.Iterable[str], password: str,
             message: EmailMessage, sender: str = None):
        if not message['From']:
            if not sender:
                message['From'] = from_addr
            else:
                message['From'] = formataddr((str(Header(sender, 'utf-8')), from_addr))

        if not message['To']:
            message['To'] = to_addr if type(to_addr) == str else ', '.join(to_addr)

        with _smtplib.SMTP_SSL(self._mail_server, self._port) as server:
            server.login(from_addr, password)
            server.send_message(message)
