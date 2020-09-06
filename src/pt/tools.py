import subprocess
import json
import time
import platform
import os
import socket

from typing import Tuple

from src.pt.exceptions import *
from src.pt import PT_EXECUTABLE, PT_BIN_ROOT, PT_GRADER
from src.commons.functions import is_port_in_use


def make_params(*args, **kwargs) -> Tuple[str, ...]:
    params = [str(arg) for arg in args]
    for name, value in kwargs.items():
        if value is not None:
            if value:
                params.append(f'--{name}')
                if type(value) != bool:
                    params.append(str(value))
    return tuple(params)


def launch_pt(port=39000, nogui=False, attempts=120, delay=500) -> subprocess.Popen:
    if platform.system() == 'Linux':
        ld_library_path = 'LD_LIBRARY_PATH'
        if not os.getenv(ld_library_path):
            os.environ[ld_library_path] = PT_BIN_ROOT

    # check if port is in use
    if is_port_in_use(port):
        raise PortInUse(port, nogui)

    params = make_params(PT_EXECUTABLE,
                         **{
                             'ipc-port': port,
                             'nogui': nogui
                         })

    process = subprocess.Popen(params,
                               cwd=PT_BIN_ROOT,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
    if process.poll():
        raise LaunchingPacketTracerError(port, nogui)

    # wait until PT is up
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(attempts):
        if not sock.connect_ex(('localhost', port)):
            break
        time.sleep(delay / 1000)
    else:
        process.kill()
        raise LaunchingPacketTracerTimeout(port, nogui)

    return process


def call_grader(filepath: str, password: str, host='localhost', port=39000, conn_attempts=5, conn_delay=100,
                alive_attempts=10, alive_delay=2000) -> dict:
    params = make_params('java', '-jar', PT_GRADER,
                         input=filepath,
                         key=password,
                         host=host,
                         port=port,
                         conn_attempts=conn_attempts,
                         conn_delay=conn_delay,
                         alive_attempts=alive_attempts,
                         alive_delay=alive_delay)

    completed_process = subprocess.run(params,
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
                return json.loads(line[first_bracket_index:last_bracket_index + 1])
            except json.JSONDecodeError:
                pass

    raise GraderNoJsonInStdout(completed_process.stdout)


if __name__ == '__main__':
    print('This is module with functions to call external grader pt')
