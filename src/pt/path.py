import os
import platform

from src import TOOLS_ROOT


def _get_pt_home():
    pt_home = os.getenv('PT7HOME')
    if pt_home:
        return pt_home
    else:
        raise FileNotFoundError('Can not find Packet Tracer home directory')


def _get_pt_bin_dir():
    return os.path.join(_get_pt_home(), 'bin')


def _get_pt_executable():
    if platform.system() == 'Windows':
        return os.path.join(_get_pt_bin_dir(), 'PacketTracer7.exe')
    elif platform.system() == 'Linux':
        return os.path.join(_get_pt_bin_dir(), 'PacketTracer7')
    else:
        raise FileNotFoundError('Can not find Packet Tracer executable')


def _get_pt_grader_root():
    return os.path.join(TOOLS_ROOT, 'grader')


def _get_pt_meta_root():
    return os.path.join(TOOLS_ROOT, 'meta')


def _get_pt_grader():
    grader = os.path.join(_get_pt_grader_root(), 'Grader.jar')
    if os.path.exists(grader):
        return grader
    else:
        raise FileNotFoundError('Can not find Grader.jar')


def _get_pt_meta():
    if platform.system() == 'Windows':
        return os.path.join(_get_pt_meta_root(), 'meta.exe')
    elif platform.system() == 'Linux':
        return os.path.join(_get_pt_meta_root(), 'meta')
    else:
        raise FileNotFoundError('Can not find Packet Tracer meta')


PT_HOME = _get_pt_home()
PT_BIN_DIR = _get_pt_bin_dir()
PT_EXECUTABLE = _get_pt_executable()

PT_GRADER_ROOT = _get_pt_grader_root()
PT_GRADER = _get_pt_grader()
