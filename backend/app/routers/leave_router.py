from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.leave import (
    LeaveRequestCreate,
    LeaveRequestResponse,
)
from app.services.leave_service import create_leave_request


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