import pytest
import tempfile

from src.pt.pt_process import PTProcess
from src.pt.exceptions import *
from test.pt.utils import *
from test.pt import *


@pytest.fixture(scope='module')
def get_pt_process():
    with PTProcess() as grade:
        yield grade


@pytest.mark.parametrize(
    ('filepath', 'password', 'expected'),
    [(filepath, password, data) for filepath, (password, data) in
     load_index(PT_DATA_ROOT).items()]
)
def test_normal(filepath, password, expected, get_pt_process):
    data = get_pt_process(filepath, password)
    assert data == expected


@pytest.mark.parametrize(
    ('filepath', 'password', 'expected'),
    [(filepath, password + 'wrong_password', data) for filepath, (password, data) in
     load_index(PT_DATA_ROOT).items()]
)
def test_wrong_password(filepath, password, expected, get_pt_process):
    with pytest.raises(GraderWrongPassword):
        get_pt_process(filepath, password)


@pytest.mark.parametrize(
    ('filename', 'content'),
    [(generate_random_filepath(0), generate_random_string(100)) for i in range(5)]
)
def test_corrupted(filename, content, get_pt_process):
    with tempfile.TemporaryDirectory(dir=DATA_ROOT) as temp_dir:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as file:
            file.write(content)
        with pytest.raises(GraderActivityFileReadingError):
            get_pt_process(filepath, 'password')
