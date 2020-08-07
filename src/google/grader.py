import typing as _typing

from src.grader.data import ClassroomPTLab
from src.grader.grader import Grader
from src.pt.data import ActivityFileData
from src.pt.exceptions import ExternalToolError
from src.commons.mailer import Mailer


class ClassroomGrader(Grader):
    def __init__(self, mailer: Mailer, parallel=False):
        super().__init__(parallel)
        self._mailer = mailer

    @staticmethod
    def get_files(dir_path: str) -> _typing.Tuple[ClassroomPTLab, ...]:
        pass

    @staticmethod
    def after_grade(grade_result: _typing.Tuple[_typing.Tuple[ClassroomPTLab, ActivityFileData, ExternalToolError],
                                                ...]):
        pass

    @staticmethod
    def process_error(error: Exception):
        pass
