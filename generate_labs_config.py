import argparse
import os

from src.settings import LABS_CONFIG_FILEPATH
from src.settings.utils import load_config, save_config
from src.commons.functions import check_file, check_dir
from src.pt.pt_process import PTProcess

INDEX_SCHEMA = {
    'type': 'object',
    'additionalProperties': {
        'type': 'object',
        'additionalProperties': {
            'type': 'object',
            'properties': {
                'filename': {'type': 'string'},
                'password': {'type': 'string'}
            }
        }
    }
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='Make labs config',
                                     description='Make labs config from lab files and index of those files')
    parser.add_argument('index',
                        metavar='INDEX',
                        help='Path to index file',
                        type=lambda x: check_file(parser, x))
    parser.add_argument('files',
                        metavar='FILES',
                        help='Path to directory with labs files',
                        type=lambda x: check_dir(parser, x))

    return parser.parse_args()


def main(index: str, files: str):
    _index = load_config(index, INDEX_SCHEMA)
    with PTProcess() as grade:
        labs = dict()
        for course_id, course_work in _index:
            labs[course_id] = dict()
            for course_work_id, data in course_work:
                filepath = os.path.join(files, data['name'])
                password = data['password']
                labs[course_id][course_work_id] = {**grade(filepath, password), **{'password': password}}
    os.makedirs(os.path.dirname(LABS_CONFIG_FILEPATH), exist_ok=True)
    save_config(labs, LABS_CONFIG_FILEPATH)


if __name__ == '__main__':
    args = parse_args()
    main(args.index, args.files)
