import abc as _abc

import src.commons.functions


class Report(_abc.ABC):
    def __init__(self, email: str, filepath: str, lab_name: str, mark: int):
        self._email = email
        self._filepath = filepath
        self._lab_name = lab_name
        self._mark = mark

    @property
    def email(self) -> str:
        return self._email

    @property
    @_abc.abstractmethod
    def html(self) -> str:
        pass


class ErrorReport(Report, _abc.ABC):
    def __init__(self, email: str, filepath: str, lab_name: str):
        super().__init__(email, filepath, lab_name, 0)


class StandardReport(Report):

    @property
    def html(self) -> str:
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
