import typing as _typing
import multiprocessing as _mp
import tempfile as _tempfile
import itertools as _itertools
import abc as _abc

import src.commons.functions

from src.grader.data import PTLab
from src.pt.data import ActivityFileData
from src.pt.exceptions import ExternalToolError
from src.pt.pt_process import PTProcess


class Singleton(_abc.ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Grader(metaclass=Singleton):
    def __init__(self, parallel=False):
        self._parallel = parallel

    @staticmethod
    def _grade(labs: _typing.Iterable[PTLab]) -> \
            _typing.Tuple[_typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        def grade(_lab: PTLab, _pt_process: PTProcess) -> \
                _typing.Tuple[ActivityFileData or None, ExternalToolError or None]:
            try:
                data = _pt_process.grade(_lab.filepath, _lab.password)
            except ExternalToolError as e:
                return None, e
            else:
                return data, None

        with PTProcess() as pt_process:
            return tuple((lab,) + grade(lab, pt_process) for lab in labs)

    @staticmethod
    def _grade_sequentially(labs: _typing.Iterable[PTLab]) -> \
            _typing.Tuple[_typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        try:
            result = Grader._grade(labs)
        except Exception as e:
            raise e
        else:
            return result

    @staticmethod
    def _grade_parallel(labs: _typing.Iterable[PTLab], process_num: int) -> \
            _typing.Tuple[_typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        chunks = src.commons.functions.get_chunks(labs, process_num)
        with _mp.Pool(process_num) as pool:
            try:
                result = pool.map(Grader._grade, chunks)
            except Exception as e:
                pool.terminate()
                raise e
            else:
                return tuple(_itertools.chain.from_iterable(result))

    @staticmethod
    def _get_optimal_process_num(labs_num: int):
        cpu_count = _mp.cpu_count()
        if labs_num < cpu_count * 4:
            return 1
        elif labs_num < cpu_count * 16 and cpu_count >= 2:
            return 2
        elif labs_num < cpu_count * 64 and cpu_count >= 4:
            return 4
        else:
            return cpu_count

    @staticmethod
    def grade(labs: _typing.Iterable[PTLab], parallel: bool) \
            -> _typing.Tuple[_typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        labs = tuple(labs)
        process_num = Grader._get_optimal_process_num(len(labs))
        if not parallel or process_num == 1:
            return Grader._grade(labs)
        else:
            return Grader._grade_parallel(labs, process_num)

    @_abc.abstractmethod
    def get_files(self, dir_path: str) -> _typing.Tuple[PTLab, ...]:
        pass

    @_abc.abstractmethod
    def after_grade(self, grade_result: _typing.Tuple[_typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]):
        pass

    @_abc.abstractmethod
    def process_error(self, error: Exception):
        pass

    def run(self):
        with _tempfile.TemporaryDirectory(dir=src.PROJECT_ROOT) as temp_dir:
            try:
                labs = self.get_files(temp_dir)
                grade_result = self.__class__.grade(labs, self._parallel)
                self.after_grade(grade_result)
            except Exception as e:
                self.process_error(e)
