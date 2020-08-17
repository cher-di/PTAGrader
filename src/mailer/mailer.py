import smtplib
import typing

from email.message import EmailMessage
from email.header import Header
from email.utils import formataddr


class Mailer:
    def __init__(self, mail_server: str):
        self._mail_server = mail_server
        self._port = 465

    def send(self, from_addr: str, to_addr: str or typing.Iterable[str], password: str,
             message: EmailMessage, sender: str = None):
        if not message['From']:
            if not sender:
                message['From'] = from_addr
            else:
                message['From'] = formataddr((str(Header(sender, 'utf-8')), from_addr))

        if not message['To']:
            message['To'] = to_addr if type(to_addr) == str else ', '.join(to_addr)

        with smtplib.SMTP_SSL(self._mail_server, self._port) as server:
            server.login(from_addr, password)
            server.send_message(message, from_addr, to_addr)


class PersonalMailer:
    def __init__(self, mail_server: str, addr: str, password: str, name: str = None):
        self._mailer = Mailer(mail_server)
        self._addr = addr
        self._password = password
        self._name = name

    def send(self, to_addr: str or typing.Iterable[str], message: EmailMessage):
        self._mailer.send(self._addr, to_addr, self._password, message, self._name)
