import os
import json
import string
import random
import time

random.seed(time.time())


def load_index(root: str) -> dict:
    index_path = os.path.join(root, 'index.json')
    with open(index_path, 'r') as file:
        index = json.load(file)
    return {os.path.join(root, filename): (data.pop('password'), data) for filename, data in index.items()}


def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_filepath(nesting: int) -> str:
    dirs = tuple(generate_random_string(random.randint(5, 10)) for i in range(nesting))
    filename = f'{generate_random_string(random.randint(5, 10))}.{generate_random_string(3)}'
    path_parts = dirs + (filename,)
    return os.path.join(*path_parts)


def generate_random_file(dirpath: str, nesting: int, content_length: int) -> str:
    filepath = os.path.join(dirpath, generate_random_filepath(nesting))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wt') as file:
        file.write(generate_random_string(content_length))
    return filepath
