from dataclasses import dataclass


@dataclass
class LaboratoryWork:
    id_: int | None = None
    number: int | None = None
    description: str | None = None
    member_credentials: str | None = None
    cloud_link: str | None = None
