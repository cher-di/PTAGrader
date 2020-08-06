import typing as _typing

from src.grader.data import ClassroomPTLab
from src.grader.grader import Grader
from src.pt.data import ActivityFileData
from src.pt.exceptions import ExternalToolError


class ClassroomGrader(Grader):
    @staticmethod
    def get_files(dir_path: str) -> _typing.Tuple[ClassroomPTLab, ...]:
        pass

    @staticmethod
    def after_grade(grade_result: _typing.Tuple[_typing.Tuple[ClassroomPTLab, ActivityFileData, ExternalToolError],
                                                ...]):
        pass
