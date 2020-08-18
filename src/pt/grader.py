import multiprocessing as mp
import itertools
import dataclasses

import src.commons.functions

from typing import Iterable, Tuple, Union, Mapping

from src.pt.tools import ActivityFileData
from src.pt.exceptions import ExternalToolError
from src.pt.pt_process import PTProcess


@dataclasses.dataclass(frozen=True)
class PTLab:
    filepath: str
    password: str


class Grader:
    def __init__(self, labs: Iterable[PTLab], parallel=False, nogui=False):
        self._labs = tuple(labs)
        self._parallel = parallel
        self._nogui = nogui

    @staticmethod
    def _grade(labs: Iterable[PTLab], nogui: bool) -> Tuple[Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        def grade(_lab: PTLab, _pt_process: PTProcess) -> Union[Tuple[ActivityFileData, ExternalToolError]]:
            try:
                data = _pt_process.grade(_lab.filepath, _lab.password)
            except ExternalToolError as e:
                return None, e
            else:
                return data, None

        with PTProcess(nogui=nogui) as pt_process:
            return tuple((lab,) + grade(lab, pt_process) for lab in labs)

    def _grade_sequentially(self) -> Tuple[Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        return self.__class__._grade(self._labs, self._nogui)

    def _grade_parallel(self, process_num: int) -> Tuple[Tuple[PTLab, ActivityFileData, ExternalToolError], ...]:
        chunks = tuple(src.commons.functions.get_chunks(self._labs, process_num))
        with mp.Pool(process_num) as pool:
            try:
                result = pool.map(lambda labs: self.__class__._grade(labs, self._nogui), chunks)
            except Exception as e:
                pool.terminate()
                raise e
            else:
                return tuple(itertools.chain.from_iterable(result))

    def _get_optimal_process_num(self):
        labs_num = len(self._labs)
        cpu_count = mp.cpu_count()
        if labs_num < cpu_count * 2:
            return 1
        elif labs_num < cpu_count * 4 and cpu_count >= 2:
            return 2
        elif labs_num < cpu_count * 8 and cpu_count >= 4:
            return 4
        else:
            return cpu_count

    def run(self):
        process_num = self._get_optimal_process_num()
        if not self._parallel or process_num == 1:
            return self._grade_sequentially()
        else:
            return self._grade_parallel(process_num)


def grade(labs: Iterable[Mapping[str, str]], parallel=False, nogui=False):
    pt_labs = (PTLab(**lab) for lab in labs)
    return Grader(pt_labs, parallel, nogui).run()
