import os
import shutil
import platform
import argparse

from src import HOME, DATA_ROOT
from src.pt import PTA_GRADER_ROOT, PT_GRADER
from src.commons.functions import check_file, check_admin_privileges

if platform.system() == 'Windows':
    PT_DATA_ROOT = os.path.join(HOME, 'Cisco Packet Tracer 7.3.1')
elif platform.system() == 'Linux':
    PT_DATA_ROOT = os.path.join(HOME, 'pt')
else:
    raise Exception(f'Unsupported OS: {platform.system()}')

PT_CONF = os.path.join(PT_DATA_ROOT, 'PT.conf')
PTA_FILE = os.path.join(PTA_GRADER_ROOT, 'PTAGrader.pta')


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

    # make data directory
    os.makedirs(DATA_ROOT, exist_ok=True)


if __name__ == '__main__':
    args = parse_args()
    main(args.grader, args.pta, args.conf)
