import dataclasses


@dataclasses.dataclass(frozen=True)
class ActivityFileData:
    name: str
    email: str
    add_info: str
    time_elapsed: int
    lab_id: str
    complete: int


def activity_data_from_grader_response(data: dict) -> ActivityFileData:
    name = data['name']
    email = data['email']
    add_info = data['addInfo']
    time_elapsed_milliseconds = data['timeElapsed']
    time_elapsed_seconds = time_elapsed_milliseconds // 1000 + 1 if time_elapsed_milliseconds % 1000 else \
        time_elapsed_milliseconds // 1000
    lab_id = data['variables']['LabID']
    complete = int(data['percentageCompleteScore'])
    return ActivityFileData(name, email, add_info, time_elapsed_seconds, lab_id, complete)
