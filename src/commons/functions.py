import socket as _socket
import typing as _typing


def get_free_port() -> int:
    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        return sock.getsockname()[1]


def is_port_in_use(port: int) -> bool:
    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('localhost', port)) == 0


def get_chunks(array: _typing.Iterable[_typing.Any], chunks: int) -> \
        _typing.Generator[_typing.Generator[_typing.Any, None, None], None, None]:
    array = tuple(array)
    for i in range(0, len(array), chunks):
        yield (element for element in array[i:i + chunks])
