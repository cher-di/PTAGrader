import os
import dataclasses
import yaml

from fastjsonschema import validate

from src import CONFIG_ROOT
from src.settings.schema import MAIN_CONFIG_SCHEMA, LABS_CONFIG_SCHEMA


__all__ = [
    'GRADER',
    'CLASSROOM',
    'MAILER',
    'LABS'
]


@dataclasses.dataclass(frozen=True)
class Lab:
    lab_id: str
    password: str


@dataclasses.dataclass(frozen=True)
class Grader:
    parallel: bool
    nogui: bool


@dataclasses.dataclass(frozen=True)
class Classroom:
    course_id: str


@dataclasses.dataclass(frozen=True)
class Mailer:
    enable_students_mailing: bool
    enable_admins_mailing: bool
    server: str
    connection: str
    port: int
    address: str
    password: str
    name: str
    admins_mail_list: str


def load_config(filepath: str, schema: dict = None) -> dict:
    with open(filepath, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    if schema:
        validate(schema, config)
    return config


MAIN_CONFIG_FILEPATH = os.path.join(CONFIG_ROOT, 'main.yaml')
LABS_CONFIG_FILEPATH = os.path.join(CONFIG_ROOT, 'labs.yaml')

MAIN_CONFIG = load_config(MAIN_CONFIG_FILEPATH, MAIN_CONFIG_SCHEMA)
LABS_CONFIG = load_config(LABS_CONFIG_FILEPATH, LABS_CONFIG_SCHEMA)

GRADER = Grader(**MAIN_CONFIG['grader'])
CLASSROOM = Classroom(MAIN_CONFIG['classroom'])
MAILER = Mailer(**MAIN_CONFIG['mailer'])
LABS = {course_work_id: Lab(**lab_data) for course_work_id, lab_data in LABS_CONFIG.items()}
