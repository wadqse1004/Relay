from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ApprovalLineCreate(BaseModel):
    approver_id: int
    sequence: int


class ApprovalDocumentCreate(BaseModel):
    document_type_id: int
    requester_id: int
    title: str
    approvers: list[ApprovalLineCreate]


class ApprovalLineResponse(BaseModel):
    id: int
    approver_id: int
    sequence: int
    status_id: int
    acted_at: datetime | None
    comment: str | None

    model_config = ConfigDict(from_attributes=True)


class ApprovalDocumentResponse(BaseModel):
    id: int
    document_no: str
    document_type_id: int
    requester_id: int
    title: str
    status_id: int
    submitted_at: datetime | None
    completed_at: datetime | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ApprovalActionRequest(BaseModel):
    approver_id: int
    comment: str | None = None

class ApprovalInboxItemResponse(BaseModel):
    document_id: int
    document_no: str
    title: str

    requester_id: int
    requester_name: str

    line_id: int
    sequence: int

    status_code: str
    status_name: str

    submitted_at: datetime | None

    leave_type_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    days: Decimal | None = None
    reason: str | None = None