import pytest
import dataclasses
import tempfile

from src.pt.grader import grade
from src.pt.exceptions import *
from test.pt.utils import *
from test.pt import *


CORRUPTED_FILES_NUM = 5


@pytest.fixture(scope='function', params=(True, False), ids=lambda x: f'parallel={x}')
def parallel(request):
    return request.param


def test_normal(parallel):
    index = load_index(PT_DATA_ROOT)
    expected = {filepath: data for filepath, (password, data) in index.items()}
    labs = {filepath: password for filepath, (password, data) in index.items()}
    graded = grade(labs, LOAD_INTERVAL, parallel)
    graded_to_dict = {filepath: dataclasses.asdict(data) for filepath, (data, error) in graded.items()}
    assert graded_to_dict == expected


def test_wrong_password(parallel):
    index = load_index(PT_DATA_ROOT)
    labs = {filepath: password + 'wrong_password' for filepath, (password, data) in index.items()}
    graded = grade(labs, LOAD_INTERVAL, parallel)
    all_data_is_none = all(data is None for data, _ in graded.values())
    all_errors_is_wrong_password = all(type(error) == GraderWrongPassword for _, error in graded.values())
    assert all_data_is_none and all_errors_is_wrong_password


@pytest.fixture(scope='function')
def generate_corrupted_files():
    with tempfile.TemporaryDirectory(dir=PT_DATA_ROOT) as temp_dir:
        files = list()
        for i in range(CORRUPTED_FILES_NUM):
            files.append(generate_random_file(temp_dir, 0, 100))
        yield files


def test_corrupted(parallel, generate_corrupted_files):
    password = generate_random_string(10)
    files = generate_corrupted_files
    labs = {filepath: password for filepath in files}
    graded = grade(labs, LOAD_INTERVAL, parallel)
    all_data_is_none = all(data is None for data, _ in graded.values())
    all_errors_is_wrong_password = all(type(error) == GraderActivityFileReadingError for _, error in graded.values())
    assert all_data_is_none and all_errors_is_wrong_password
