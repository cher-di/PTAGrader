from src.settings.utils import load_config
from src.settings import MAIN_CONFIG_FILEPATH, LABS_CACHE_FILEPATH
from src.settings.schema import MAIN_CONFIG_SCHEMA
from src.settings.format import *


__all__ = [
    'GRADER',
    'CLASSROOM',
    'MAILER',
    'LABS'
]

MAIN_CONFIG = load_config(MAIN_CONFIG_FILEPATH, MAIN_CONFIG_SCHEMA)
LABS_CACHE = load_config(LABS_CACHE_FILEPATH)

GRADER = Grader(**MAIN_CONFIG['grader'])
CLASSROOM = Classroom(MAIN_CONFIG['classroom'])
MAILER = Mailer(**MAIN_CONFIG['mailer'])

LABS = dict()
for course_id, course_work in LABS_CACHE.items():
    LABS[course_id] = dict()
    for course_work_id, data in course_work:
        LABS[course_id][course_work_id] = Lab(**data)
