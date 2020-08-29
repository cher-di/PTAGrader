import smtplib
import copy

from abc import ABC, abstractmethod
from typing import Iterable, Union

from email.utils import formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart


class Mailer(ABC):
    def __init__(self, server: str, port: int, address: str, password: str, name: str = None):
        self._server = server
        self._port = port
        self._address = address
        self._password = password
        self._name = name

    def __enter__(self) -> 'Mailer':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def _add_from_and_to(from_address: str, to_address: str, message: MIMEMultipart, name: str = None) -> MIMEMultipart:
        new_message = copy.copy(message)
        if name:
            from_address = formataddr((str(Header(name, 'utf-8')), from_address))
        new_message['From'] = from_address
        new_message['To'] = to_address
        return new_message

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        pass


class SMTPLIBMailer(Mailer, ABC):
    def __init__(self, server: str, port: int, address: str, password: str, name: str = None):
        super().__init__(server, port, address, password, name)
        self._connection: smtplib.SMTP = None

    def close(self):
        self._connection.close()

    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        if not self._connection:
            raise ConnectionError(f'Mailer is not connected to SMTP server {self._server}')
        new_message = self.__class__._add_from_and_to(self._address, address, message, self._name)
        self._connection.sendmail(self._address, address, new_message.as_string())

    def _auth(self):
        self._connection.login(self._address, self._password)

    @abstractmethod
    def _open(self):
        pass

    def open(self):
        self._open()
        self._auth()


class SSLMailer(SMTPLIBMailer):
    def __init__(self, server: str, address: str, password: str, name: str = None, port=465):
        super().__init__(server, port, address, password, name)

    def _open(self):
        self._connection = smtplib.SMTP_SSL(self._server, self._port)


class TLSMailer(SMTPLIBMailer):
    def __init__(self, server: str, address: str, password: str, name: str = None, port=587):
        super().__init__(server, port, address, password, name)

    def _open(self):
        self._connection = smtplib.SMTP(self._server, self._port)
        self._connection.starttls()
