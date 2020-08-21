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

    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        with smtplib.SMTP_SSL(self._server, self._port) as server:
            server.login(self._address, self._password)
            new_message = self.__class__._add_from_and_to(self._address, address, message, self._name)
            server.send_message(new_message, self._address, address)


class TLSMailer(Mailer):
    def __init__(self, server: str, address: str, password: str, name: str = None):
        super().__init__(server, 587, address, password, name)

    def send(self, address: Union[str, Iterable[str]], message: MIMEMultipart):
        with smtplib.SMTP(self._server, self._port) as server:
            server.starttls()
            server.login(self._address, self._password)
            new_message = self.__class__._add_from_and_to(self._address, address, message, self._name)
            server.send_message(new_message, self._address, address)
