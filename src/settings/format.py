import dataclasses


@dataclasses.dataclass(frozen=True)
class Grader:
    parallel: bool
    nogui: bool


@dataclasses.dataclass(frozen=True)
class Classroom:
    course_id: str


@dataclasses.dataclass(frozen=True)
class Mailer:
    enable_students_mailing: bool
    enable_admins_mailing: bool
    server: str
    connection: str
    port: int
    address: str
    password: str
    name: str
    admins_mail_list: str
