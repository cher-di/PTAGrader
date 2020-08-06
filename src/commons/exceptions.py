class PTAGraderError(Exception):
    pass


class CommonPTAGraderError(PTAGraderError):
    pass


class PortInUse(CommonPTAGraderError):
    def __init__(self, port: int):
        self._port = port

    def __str__(self):
        return f'Port {self._port} is already in use'

    @property
    def port(self) -> int:
        return self._port
