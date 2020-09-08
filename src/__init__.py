import os

from pathlib import Path

SOURCE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(SOURCE_ROOT)
RESOURCES_ROOT = os.path.join(PROJECT_ROOT, 'res')

HOME = str(Path().home())
DATA_ROOT = os.path.join(HOME, '.PTAGrader')
CONFIG_ROOT = os.path.join(DATA_ROOT, 'config')
FILES_ROOT = os.path.join(DATA_ROOT, 'files')
