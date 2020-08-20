import subprocess

import src.pt.tools
import src.pt.exceptions
import src.commons.functions

from src.pt.tools import ActivityFileData


class PTProcess:
    def __init__(self, load_interval: int, port: int = None, nogui=False):
        if not port:
            self._port = src.commons.functions.get_free_port()
        else:
            if src.commons.functions.is_port_in_use(port):
                raise src.pt.exceptions.PortInUse(port, load_interval, nogui)
            else:
                self._port = port
        self._load_interval = load_interval
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
        return src.pt.tools.call_grader(filepath, password, port=self._port)

    def start(self):
        if not self._process:
            self._process = src.pt.tools.launch_pt(self._port, self._nogui, self._load_interval)
        else:
            raise src.pt.exceptions.PTProcessAlreadyRunningError(self._port, self._load_interval, self._nogui)

    def stop(self):
        if self._process:
            self._process.kill()
            self._process = None
        else:
            raise src.pt.exceptions.PTProcessNotStarted(self._port, self._load_interval, self._nogui)
