import os
import shutil
import platform
import argparse
import ctypes
import dataclasses

from pathlib import Path

from src import FILES_ROOT
from src.settings import LABS_CONFIG_FILEPATH, LABS_CACHE_FILEPATH
from src.settings.utils import load_config, save_config
from src.settings.schema import LABS_CONFIG_SCHEMA
from src.settings.format import Lab
from src.pt import PTA_GRADER_ROOT, PT_GRADER
from src.pt.pt_process import PTProcess

HOME = str(Path().home())

if platform.system() == 'Windows':
    PT_DATA_ROOT = os.path.join(HOME, 'Cisco Packet Tracer 7.3.1')
elif platform.system() == 'Linux':
    PT_DATA_ROOT = os.path.join(HOME, 'pt')
else:
    raise Exception(f'Unsupported OS: {platform.system()}')

PT_CONF = os.path.join(PT_DATA_ROOT, 'PT.conf')
PTA_FILE = os.path.join(PTA_GRADER_ROOT, 'PTAGrader.pta')


def check_file(parser: argparse.ArgumentParser, filepath: str):
    if not os.path.isfile(filepath):
        parser.error(f'{filepath} not exists')
    return filepath


def check_admin_privileges() -> bool:
    if platform.system() == 'Windows':
        return ctypes.windll.shell32.IsUserAnAdmin()
    elif platform.system() == 'Linux':
        return os.getuid() == 0
    else:
        raise Exception(f'Unsupported OS: {platform.system()}')


def parse_args():
    parser = argparse.ArgumentParser(prog='Setup PTAGrader to your machine',
                                     description="""Before running this utility, download Grader.jar, PTAGrader.pta and
                                     PT.conf. Grader.jar and PTAGrader.pta are cross-platform, PT.conf is platform dependent.
                                     After that start this utility with paths to downloaded files.""",
                                     epilog="""It is strongly recommended to run this utility right after PacketTracer
                                     installation!
                                     Run this utility only when PacketTracer is switched off!
                                     You must invoke root privileges before running this script!""")
    parser.add_argument('grader',
                        metavar='GRADER',
                        help='Path to Grader.jar file',
                        type=lambda x: check_file(parser, x))
    parser.add_argument('conf',
                        metavar='CONF',
                        help='Path to PT.conf file',
                        type=lambda x: check_file(parser, x))
    parser.add_argument('pta',
                        metavar='PTA',
                        help='Path to PTAGrader.pta file',
                        type=lambda x: check_file(parser, x))

    return parser.parse_args()


def main(grader: str, pta_file: str, pt_conf: str):
    # check if script run as root
    if not check_admin_privileges():
        raise Exception('Run this script with admin privileges')

    # make PT extension
    os.makedirs(PTA_GRADER_ROOT, exist_ok=True)
    shutil.copyfile(grader, PT_GRADER)
    shutil.copyfile(pta_file, PTA_FILE)

    # change PT.conf
    os.makedirs(PT_DATA_ROOT, exist_ok=True)
    shutil.copyfile(pt_conf, PT_CONF)

    # create labs_cache.yaml
    files = dict()
    labs = load_config(LABS_CONFIG_FILEPATH, LABS_CONFIG_SCHEMA)
    with PTProcess() as pt_process:
        for course_id, course_work in labs:
            files[course_id] = dict()
            for course_work_id, data in course_work:
                password = data['password']
                filepath = os.path.join(FILES_ROOT, data['filename'])
                content = pt_process.grade(filepath, password)
                lab = Lab(**dataclasses.asdict(content), password=password)
                files[course_id][course_work_id] = dataclasses.asdict(lab)
    save_config(files, LABS_CACHE_FILEPATH)


if __name__ == '__main__':
    args = parse_args()
    main(args.grader, args.pta, args.conf)
