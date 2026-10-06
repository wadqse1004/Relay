from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave_balance import LeaveBalance
from app.models.leave_request import LeaveRequest


def find_leave_balance(
    db: Session,
    user_id: int,
    year: int,
) -> LeaveBalance | None:
    stmt = select(LeaveBalance).where(
        LeaveBalance.user_id == user_id,
        LeaveBalance.year == year,
    )

    return db.scalar(stmt)


def add_leave_request(
    db: Session,
    leave_request: LeaveRequest,
) -> LeaveRequest:
    db.add(leave_request)
    db.flush()

    return leave_request

def find_leave_request_by_document_id(
    db: Session,
    document_id: int,
) -> LeaveRequest | None:
    stmt = select(LeaveRequest).where(
        LeaveRequest.approval_document_id == document_id,
        LeaveRequest.is_active.is_(True),
    )

    return db.scalar(stmt)