from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class LeaveRequestCreate(BaseModel):
    user_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    days: Decimal
    reason: str | None = None
    approver_ids: list[int]


class LeaveRequestResponse(BaseModel):
    id: int
    approval_document_id: int
    user_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    days: Decimal
    reason: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LeaveBalanceResponse(BaseModel):
    id: int
    user_id: int
    year: int
    total_days: Decimal
    used_days: Decimal
    remaining_days: Decimal

    model_config = ConfigDict(from_attributes=True)

class LeaveRequestListResponse(BaseModel):
    id: int
    approval_document_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    days: Decimal
    reason: str | None
    status_code: str
    status_name: str
    created_at: datetime