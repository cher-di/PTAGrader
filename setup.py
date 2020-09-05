import os
import shutil
import platform
from pathlib import Path

from src import PROJECT_ROOT
from src.pt import PTA_GRADER_ROOT

BIN_ROOT = os.path.join(PROJECT_ROOT, 'bin')
GRADER = 'Grader.jar'
PT_CONF = 'PT.conf'
PTA_FILE = 'PTAGrader.pta'

HOME = str(Path().home())

if platform.system() == 'Windows':
    PT_DATA_ROOT = os.path.join(HOME, 'Cisco Packet Tracer 7.3.1')
elif platform.system() == 'Linux':
    PT_DATA_ROOT = os.path.join(HOME, 'pt')
else:
    raise OSError(f'Unsupported OS: {platform.system()}')


def check_file(filepath: str):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(filepath)


if __name__ == '__main__':
    # check binaries
    for filename in (GRADER, PT_CONF, PTA_FILE):
        check_file(os.path.join(BIN_ROOT, filename))

    # make PT extension
    os.mkdir(PTA_GRADER_ROOT)
    for filename in (GRADER, PTA_FILE):
        shutil.copyfile(os.path.join(BIN_ROOT, filename), os.path.join(PTA_GRADER_ROOT, filename))

    # make PT data directory
    os.mkdir(PT_DATA_ROOT)
    shutil.copyfile(os.path.join(BIN_ROOT, PT_CONF), os.path.join(PT_DATA_ROOT, PT_CONF))
