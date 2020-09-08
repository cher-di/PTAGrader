import json

from fastjsonschema import validate


def load_config(filepath: str, schema: dict = None) -> dict:
    with open(filepath, 'r') as file:
        config = json.load(file)
    if schema:
        validate(schema, config)
    return config


def save_config(data: dict, filepath: str):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
