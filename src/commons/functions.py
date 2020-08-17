import socket

from typing import Tuple, Any, Iterable, Generator


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        return sock.getsockname()[1]


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('localhost', port)) == 0


def get_chunks(array: Iterable[Any], chunks: int) -> Generator[Tuple[Any, ...], None, None]:
    array = tuple(array)
    array_len = len(array)
    chunk_len = array_len // chunks
    for i in range(0, len(array), chunk_len):
        yield tuple(element for element in array[i:i + chunk_len])
