import abc

DEFAULT_ERROR_MARK = 0


class Report(abc.ABC):
    def __init__(self, name: str, lab_name: str, mark: int):
        self._name = name
        self._lab_name = lab_name
        self._mark = mark

    @property
    @abc.abstractmethod
    def html(self) -> str:
        pass


class ErrorReport(Report, abc.ABC):
    def __init__(self, email: str, lab_name: str):
        super().__init__(email, lab_name, DEFAULT_ERROR_MARK)


class StandardReport(Report):

    @property
    def html(self) -> str:
        pass


class CorruptedFileReport(ErrorReport):

    @property
    def html(self) -> str:
        pass


class WrongLabReport(ErrorReport):
    def __init__(self, name: str, lab_name: str, extracted_lab_name: str):
        super().__init__(name, lab_name)
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
    def __init__(self, name: str, lab_name: str, real_email: str, extracted_email: str):
        super().__init__(name, lab_name)
        self._real_email = real_email
        self._extracted_email = extracted_email

    @property
    def html(self) -> str:
        pass
