import os
import dataclasses
import yaml

from typing import Dict
from fastjsonschema import validate

from src import CONFIG_ROOT


@dataclasses.dataclass(frozen=True)
class Lab:
    lab_id: str
    password: str


@dataclasses.dataclass(frozen=True)
class Grader:
    parallel: bool
    load_interval: int
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
    admins_mail_list: str


@dataclasses.dataclass(frozen=True)
class Settings:
    grader: Grader
    classroom: Classroom
    mailer: Mailer
    labs: Dict[str, Lab]


def load_config(filepath: str, schema: dict = None) -> dict:
    with open(filepath, 'r') as file:
        config = yaml.load(file)
    if schema:
        validate(schema, config)
    return config


MAIN_CONFIG_FILEPATH = os.path.join(CONFIG_ROOT, 'main.yaml')
LABS_CONFIG_FILEPATH = os.path.join(CONFIG_ROOT, 'labs.yaml')

MAIN_CONFIG = load_config(MAIN_CONFIG_FILEPATH)
LABS_CONFIG = load_config(LABS_CONFIG_FILEPATH)

SETTINGS = Settings(**{**MAIN_CONFIG, **{'labs': LABS_CONFIG}})
