import pytest
import tempfile

from src.pt.exceptions import *
from src.pt.tools import call_grader, launch_pt
from src.commons.functions import get_free_port
from test.pt.utils import *
from test.pt import *


@pytest.fixture(scope='module')
def run_pt():
    port = get_free_port()
    process = launch_pt(port)
    yield port
    process.kill()


@pytest.mark.parametrize(
    ('filepath', 'password', 'expected'),
    [(filepath, password, data) for filepath, (password, data) in
     load_index(PT_DATA_ROOT).items()]
)
def test_connection_error(filepath, password, expected):
    with pytest.raises(GraderConnectionError):
        call_grader(filepath, password, port=get_free_port())


@pytest.mark.parametrize(
    ('filename', 'content'),
    [(generate_random_filepath(0), generate_random_string(100)) for i in range(5)]
)
def test_corrupted(filename, content, run_pt):
    with tempfile.TemporaryDirectory(dir=DATA_ROOT) as temp_dir:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as file:
            file.write(content)
        with pytest.raises(GraderActivityFileReadingError):
            call_grader(filepath, 'password', port=run_pt)
