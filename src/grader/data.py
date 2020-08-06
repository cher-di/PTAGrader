import dataclasses as _dataclasses


@_dataclasses.dataclass(frozen=True)
class PTLab:
    email: str
    filepath: str
    password: str
    lab_id: str


@_dataclasses.dataclass(frozen=True)
class ClassroomPTLab(PTLab):
    pass
