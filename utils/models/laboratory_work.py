from dataclasses import dataclass


@dataclass
class LaboratoryWork:
    lab_id: int | None = None
    lab_number: int | None = None
    lab_description: str | None = None
    member_credentials: str | None = None
    cloud_link: str | None = None
