import abc
import typing

from email.mime.base import MIMEBase
from email.message import EmailMessage

from src.commons.mailer import PersonalMailer


class Report(abc.ABC):
    def __init__(self,
                 email: str,
                 filepath: str,
                 lab_name: str,
                 mark: int,
                 email_subject: str):
        self._email = email
        self._filepath = filepath
        self._lab_name = lab_name
        self._mark = mark
        self._email_subject = email_subject

    @abc.abstractmethod
    def get_html(self) -> str:
        pass

    @abc.abstractmethod
    def get_html_attachments(self) -> typing.Tuple[MIMEBase]:
        pass

    def send(self, mailer: PersonalMailer):
        message = EmailMessage()
        message['Subject'] = self._email_subject
        message.set_content(self.get_html(), subtype='html')
        for attach in self.get_html_attachments():
            message.attach(attach)
        mailer.send(self._email, message)


class ErrorReport(Report, abc.ABC):
    def __init__(self,
                 email: str,
                 filepath: str,
                 lab_name: str,
                 email_subject: str):
        super().__init__(email, filepath, lab_name, 0, email_subject)


class StandardReport(Report):

    @property
    def get_html(self) -> str:
        pass


class CorruptedFileReport(ErrorReport):

    @property
    def html(self) -> str:
        pass


class WrongLabReport(ErrorReport):
    def __init__(self, email: str, filepath: str, lab_name: str, extracted_lab_name: str):
        super().__init__(email, filepath, lab_name)
        self._extracted_lab_name = extracted_lab_name

    @property
    def html(self) -> str:
        pass

    @property
    def extracted_lab_name(self) -> str:
        return self._extracted_lab_name


class NotLabReport(ErrorReport):

    @property
    def html(self) -> str:
        pass


class WrongEmailReport(ErrorReport):
    def __init__(self, email: str, filepath: str, lab_name: str, extracted_email: str):
        super().__init__(email, filepath, lab_name)
        self._extracted_email = extracted_email

    @property
    def html(self) -> str:
        pass
