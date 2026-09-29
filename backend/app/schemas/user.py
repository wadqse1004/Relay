from datetime import date

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    employee_no: str
    email: str
    name: str
    birth_date: date | None
    department_id: int | None
    manager_id: int | None
    position_id: int | None
    job_title_id: int | None
    status_id: int | None
    join_date: date | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)