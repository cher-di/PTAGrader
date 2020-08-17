import typing
import multiprocessing as mp
import itertools
import dataclasses

import src.commons.functions

from src.pt.tools import ActivityFileData
from src.pt.exceptions import ExternalToolError
from src.pt.pt_process import PTProcess


@dataclasses.dataclass(frozen=True)
class PTLab:
    filepath: str
    password: str


class Grader:
    def __init__(self, labs: typing.Iterable[PTLab], parallel=False):
        self._labs = tuple(labs)
        self._parallel = parallel

    @staticmethod
    def _grade(labs: typing.Iterable[PTLab]) -> \
            typing.Tuple[typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        def grade(_lab: PTLab, _pt_process: PTProcess) -> \
                typing.Tuple[ActivityFileData or None, ExternalToolError or None]:
            try:
                data = _pt_process.grade(_lab.filepath, _lab.password)
            except ExternalToolError as e:
                return None, e
            else:
                return data, None

        with PTProcess() as pt_process:
            return tuple((lab,) + grade(lab, pt_process) for lab in labs)

    def _grade_sequentially(self) -> typing.Tuple[typing.Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        return self.__class__._grade(self._labs)

    def _grade_parallel(self, process_num: int) -> typing.Tuple[typing.Tuple[PTLab, ActivityFileData,
                                                                             ExternalToolError], ...]:
        chunks = src.commons.functions.get_chunks(self._labs, process_num)
        with mp.Pool(process_num) as pool:
            try:
                result = pool.map(self.__class__._grade, chunks)
            except Exception as e:
                pool.terminate()
                raise e
            else:
                return tuple(itertools.chain.from_iterable(result))

    def _get_optimal_process_num(self):
        labs_num = len(self._labs)
        cpu_count = mp.cpu_count()
        if labs_num < cpu_count * 4:
            return 1
        elif labs_num < cpu_count * 16 and cpu_count >= 2:
            return 2
        elif labs_num < cpu_count * 64 and cpu_count >= 4:
            return 4
        else:
            return cpu_count

    def run(self):
        process_num = self._get_optimal_process_num()
        if not self._parallel or process_num == 1:
            return self._grade_sequentially()
        else:
            return self._grade_parallel(process_num)
