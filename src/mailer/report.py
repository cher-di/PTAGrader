import abc
import jinja2
import os

from src import RESOURCES_ROOT

TEMPLATES_ROOT = os.path.join(RESOURCES_ROOT, 'templates')

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_ROOT),
)

DEFAULT_ERROR_MARK = 0


class Report(abc.ABC):
    def __init__(self, name: str, lab_name: str, mark: int):
        self._name = name
        self._lab_name = lab_name
        self._mark = mark
        template = env.get_template(self.html_template)
        self._html = template.render(self.parameters)

    @property
    def parameters(self) -> dict:
        return {
            'name': self._name,
            'lab_name': self._lab_name,
            'mark': self._mark,
        }

    @property
    @abc.abstractmethod
    def html_template(self) -> str:
        pass

    @property
    def html(self) -> str:
        return self._html


class ErrorReport(Report, abc.ABC):
    def __init__(self, name: str, lab_name: str):
        super().__init__(name, lab_name, DEFAULT_ERROR_MARK)


class StandardReport(Report):

    @property
    def html_template(self) -> str:
        return 'standard.html'


class CorruptedFileReport(ErrorReport):

    @property
    def html_template(self) -> str:
        return 'corrupted_file.html'


class WrongLabReport(ErrorReport):
    def __init__(self, name: str, lab_name: str, extracted_lab_name: str):
        super().__init__(name, lab_name)
        self._extracted_lab_name = extracted_lab_name

    @property
    def parameters(self) -> dict:
        parameters = super().parameters
        parameters['extracted_lab_name'] = self._extracted_lab_name
        return parameters

    @property
    def html_template(self) -> str:
        return 'wrong_lab.html'


class NotLabReport(ErrorReport):

    @property
    def html_template(self) -> str:
        return 'not_lab.html'


class WrongEmailReport(ErrorReport):
    def __init__(self, name: str, lab_name: str, real_email: str, extracted_email: str):
        super().__init__(name, lab_name)
        self._real_email = real_email
        self._extracted_email = extracted_email

    @property
    def parameters(self) -> dict:
        parameters = super().parameters
        parameters['real_email'] = self._real_email
        parameters['extracted_email'] = self._extracted_email
        return parameters

    @property
    def html_template(self) -> str:
        return 'wrong_email.html'
