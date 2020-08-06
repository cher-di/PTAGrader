import dataclasses as _dataclasses


@_dataclasses.dataclass(frozen=True)
class ActivityFileData:
    name: str
    email: str
    percentageComplete: float
    percentageCompleteScore: float
    addInfo: str
    timeElapsed: int
    labID: str
