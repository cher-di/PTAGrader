import os
import shutil

from src import CONFIG_ROOT, RESOURCES_ROOT
from src.pt.path import PT_GRADER_ROOT

CONFIG_TEMPLATES_ROOT = os.path.join(RESOURCES_ROOT, 'config')

if __name__ == '__main__':
    # copy configs from templates
    shutil.copytree(CONFIG_TEMPLATES_ROOT, CONFIG_ROOT, dirs_exist_ok=True)

    # make directories for tools
    os.makedirs(PT_GRADER_ROOT, exist_ok=True)
