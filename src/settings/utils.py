import yaml

from fastjsonschema import validate


def load_config(filepath: str, schema: dict = None) -> dict:
    with open(filepath, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    if schema:
        validate(schema, config)
    return config


def save_config(data: dict, filepath: str):
    with open(filepath, 'w') as file:
        yaml.dump(data, file)