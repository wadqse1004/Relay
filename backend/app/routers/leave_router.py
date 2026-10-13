from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.leave import (
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveBalanceResponse,
)
from app.services.leave_service import (
    create_leave_request,
    get_leave_balance,
    get_leave_requests,
)
from app.schemas.leave import (
    LeaveRequestListResponse,
)

router = APIRouter(
    prefix="/api/leaves",
    tags=["Leaves"],
)


@router.post(
    "",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave(
    request: LeaveRequestCreate,
    db: Session = Depends(get_db),
):
    return create_leave_request(
        db=db,
        request=request,
    )

@router.get(
    "/balance",
    response_model=LeaveBalanceResponse,
)
def get_balance(
    user_id: int,
    year: int,
    db: Session = Depends(get_db),
):
    return get_leave_balance(
        db=db,
        user_id=user_id,
        year=year,
    )

@router.get(
    "",
    response_model=list[LeaveRequestListResponse],
)
def get_leaves(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_leave_requests(
        db=db,
        user_id=user_id,
    )