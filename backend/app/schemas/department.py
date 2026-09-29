from pydantic import BaseModel, ConfigDict


class DepartmentResponse(BaseModel):
    id: int
    code: str
    name: str
    parent_id: int | None
    description: str | None
    sort_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)