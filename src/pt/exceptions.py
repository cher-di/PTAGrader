class ExternalToolError(Exception):
    pass


class LaunchingPacketTracerError(ExternalToolError):
    def __init__(self, port: int, nogui: bool):
        super().__init__()
        self._port = port
        self._nogui = nogui

    def __str__(self):
        return f'An error occurred while launching Packet Tracer on port {self._port} with nogui={self._nogui}'

    @property
    def port(self) -> int:
        return self._port

    @property
    def nogui(self) -> bool:
        return self._nogui


class GraderError(ExternalToolError):
    pass


class GraderGeneralError(GraderError):
    pass


class GraderWrongCredentials(GraderError):
    pass


class GraderConnectionError(GraderError):
    pass


class GraderArgumentsParsingError(GraderError):
    pass


class GraderActivityFileReadingError(GraderError):
    pass


class GraderWrongPassword(GraderError):
    def __init__(self, message: str, password: str):
        super().__init__(message)
        self._password = password

    @property
    def password(self) -> str:
        return self._password


class MetaRunningError(ExternalToolError):
    def __init__(self, xml_filepath: str, pta_filepath: str):
        self._xml_filepath = xml_filepath
        self._pta_filepath = pta_filepath

    def __str__(self):
        return f'An error occurred while running meta with xml: {self._xml_filepath} and pta: {self._pta_filepath}'


class PTProcessError(Exception):
    def __init__(self, port: int, nogui: bool):
        self._port = port
        self._nogui = nogui

    @property
    def port(self) -> int:
        return self._port

    @property
    def nogui(self) -> bool:
        return self._nogui


class PTProcessAlreadyRunningError(PTProcessError):
    def __str__(self):
        return f'This instance of PTProcess with port {self._port} and nogui={self._nogui} is already running'


class PTProcessNotStarted(PTProcessError):
    def __str__(self):
        return f'This instance of PTProcess with port {self._port} and nogui={self._nogui} is not started'


class PortInUse(PTProcessError):
    def __str__(self):
        return f'Port {self._port} is already in use'
