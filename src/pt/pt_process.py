import subprocess

import src.pt.tools
import src.pt.exceptions

from src.commons.functions import get_free_port

from src.pt.activity_file_data import ActivityFileData


class PTProcess:
    def __init__(self, port: int = None, nogui=False):
        self._port = port if port else get_free_port()
        self._nogui = nogui
        self._process: subprocess.Popen = None

    def __enter__(self) -> 'PTProcess':
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return f'{self.__class__}({self._port, self._nogui})'

    def grade(self, filepath: str, password: str) -> ActivityFileData:
        data = src.pt.tools.call_grader(filepath, password, port=self._port)
        return ActivityFileData(**data)

    def start(self):
        if not self._process:
            self._process = src.pt.tools.launch_pt(self._port, self._nogui)
        else:
            raise src.pt.exceptions.PTProcessAlreadyRunningError(self._port, self._nogui)

    def stop(self):
        if self._process:
            self._process.kill()
            self._process = None
        else:
            raise src.pt.exceptions.PTProcessNotStarted(self._port, self._nogui)
