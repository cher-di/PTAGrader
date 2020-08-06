import os as _os
import platform as _platform


from src import TOOLS_ROOT


def _get_pt_home():
    pt_home = _os.getenv('PT7HOME')
    if pt_home:
        return pt_home
    else:
        raise FileNotFoundError('Can not find Packet Tracer home directory')


def _get_pt_bin_dir():
    return _os.path.join(_get_pt_home(), 'bin')


def _get_pt_executable():
    if _platform.system() == 'Windows':
        return _os.path.join(_get_pt_bin_dir(), 'PacketTracer7.exe')
    elif _platform.system() == 'Linux':
        return _os.path.join(_get_pt_bin_dir(), 'PacketTracer7')
    else:
        raise FileNotFoundError('Can not find Packet Tracer executable')


def _get_pt_meta():
    if _platform.system() == 'Windows':
        return _os.path.join(_get_pt_bin_dir(), 'meta.exe')
    elif _platform.system() == 'Linux':
        return _os.path.join(_get_pt_bin_dir(), 'meta')
    else:
        raise FileNotFoundError('Can not find Packet Tracer meta')


PT_HOME = _get_pt_home()
PT_BIN_DIR = _get_pt_bin_dir()
PT_EXECUTABLE = _get_pt_executable()
PT_META = _get_pt_meta()

PT_GRADER = _os.path.join(TOOLS_ROOT, 'Grader.jar')
