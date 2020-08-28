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
        self._connection = None

    @abstractmethod
    def __enter__(self) -> 'Mailer':
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _add_from_and_to(from_address: str, to_address: str, message: MIMEMultipart, name: str = None) -> MIMEMultipart:
        new_message = copy.copy(message)
        if name:
            from_address = formataddr((str(Header(name, 'utf-8')), from_address))
        new_message['From'] = from_address
        new_message['To'] = to_address
        return new_message

    @abstractmethod
    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        pass


class SSLMailer(Mailer):
    def __init__(self, server: str, address: str, password: str, name: str = None):
        super().__init__(server, 465, address, password, name)

    def __enter__(self) -> 'SSLMailer':
        self._connection = smtplib.SMTP_SSL(self._server, self._port)
        self._connection.login(self._address, self._password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        new_message = self.__class__._add_from_and_to(self._address, address, message, self._name)
        self._connection.sendmail(self._address, address, new_message.as_string())


class TLSMailer(Mailer):
    def __init__(self, server: str, address: str, password: str, name: str = None):
        super().__init__(server, 587, address, password, name)

    def __enter__(self) -> 'TLSMailer':
        self._connection = smtplib.SMTP(self._server, self._port)
        self._connection.starttls()
        self._connection.login(self._address, self._password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        new_message = self.__class__._add_from_and_to(self._address, address, message, self._name)
        self._connection.sendmail(self._address, address, new_message.as_string())
