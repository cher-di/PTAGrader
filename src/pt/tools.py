import subprocess
import json
import time
import dataclasses

from src.pt.exceptions import *
from src.pt.path import *


@dataclasses.dataclass(frozen=True)
class ActivityFileData:
    name: str
    email: str
    add_info: str = dataclasses.field(init=False)
    time_elapsed: int = dataclasses.field(init=False)
    lab_id: str = dataclasses.field(init=False)
    complete: int = dataclasses.field(init=False)
    addInfo: dataclasses.InitVar[str]
    timeElapsed: dataclasses.InitVar[int]
    labID: dataclasses.InitVar[str]
    percentageComplete: dataclasses.InitVar[float]
    percentageCompleteScore: dataclasses.InitVar[float]

    def __post_init__(self, addInfo: str, timeElapsed: int, labID: str, percentageComplete: float,
                      percentageCompleteScore: float):
        object.__setattr__(self, 'add_info', addInfo)
        object.__setattr__(self, 'time_elapsed', timeElapsed // 1000 + 1 if timeElapsed % 1000 else timeElapsed // 1000)
        object.__setattr__(self, 'lab_id', labID)
        object.__setattr__(self, 'complete', int(percentageCompleteScore))


def launch_pt(port=39000, nogui=False, load_interval=10) -> subprocess.Popen:
    if platform.system() == 'Linux':
        ld_library_path = 'LD_LIBRARY_PATH'
        if not os.getenv(ld_library_path):
            os.environ[ld_library_path] = PT_BIN_DIR

    process = subprocess.Popen((PT_EXECUTABLE, '--ipc-port', str(port), '--no-gui' if nogui else ''),
                               cwd=PT_BIN_DIR,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
    time.sleep(load_interval)
    if process.poll():
        raise LaunchingPacketTracerError(port, nogui)
    return process


def call_grader(filepath: str, password: str, attempts=10, delay=500, host='localhost',
                port=39000) -> ActivityFileData:
    completed_process = subprocess.run(('java', '-jar', PT_GRADER, '--input', filepath,
                                        '--key', password, '--attempts', str(attempts), '--delay', str(delay),
                                        '--host', host, '--port', str(port)),
                                       capture_output=True,
                                       text=True)

    if completed_process.returncode:
        if completed_process.returncode == 1:
            raise GraderGeneralError(completed_process.stderr)
        elif completed_process.returncode == 2:
            raise GraderWrongCredentials(completed_process.stderr)
        elif completed_process.returncode == 3:
            raise GraderConnectionError(completed_process.stderr)
        elif completed_process.returncode == 4:
            raise GraderArgumentsParsingError(completed_process.stderr)
        elif completed_process.returncode == 5:
            raise GraderActivityFileReadingError(completed_process.stderr)
        elif completed_process.returncode == 7:
            raise GraderWrongPassword(completed_process.stderr, password)
        else:
            raise GraderError(completed_process.stderr)

    for line in completed_process.stdout.split(os.linesep):
        first_bracket_index = line.find('{')
        last_bracket_index = line.rfind('}')
        if first_bracket_index != -1 and last_bracket_index != -1:
            try:
                data = json.loads(line[first_bracket_index:last_bracket_index + 1])
                return ActivityFileData(**data)
            except json.JSONDecodeError:
                pass


if __name__ == '__main__':
    print('This is module with functions to call external grader pt')
