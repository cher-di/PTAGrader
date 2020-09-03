import dataclasses


@dataclasses.dataclass(frozen=True)
class ActivityFileData:
    name: str
    email: str
    add_info: str = dataclasses.field(init=False)
    time_elapsed: int = dataclasses.field(init=False)
    lab_id: str = dataclasses.field(init=False)
    complete: int = dataclasses.field(init=False)
    addInfo: dataclasses.InitVar[str]
    timeElapsed: dataclasses.InitVar[int]
    labID: dataclasses.InitVar[str]
    percentageComplete: dataclasses.InitVar[float]
    percentageCompleteScore: dataclasses.InitVar[float]

    def __post_init__(self, addInfo: str, timeElapsed: int, labID: str, percentageComplete: float,
                      percentageCompleteScore: float):
        object.__setattr__(self, 'add_info', addInfo)
        object.__setattr__(self, 'time_elapsed', timeElapsed // 1000 + 1 if timeElapsed % 1000 else timeElapsed // 1000)
        object.__setattr__(self, 'lab_id', labID)
        object.__setattr__(self, 'complete', int(percentageCompleteScore))
