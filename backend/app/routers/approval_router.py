from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.approval import (
    ApprovalDocumentCreate,
    ApprovalDocumentResponse,
)
from app.services import approval_service


router = APIRouter(
    prefix="/api/approvals",
    tags=["Approvals"],
)


@router.post(
    "",
    response_model=ApprovalDocumentResponse,
    status_code=201,
)
def create_approval(
    request: ApprovalDocumentCreate,
    db: Session = Depends(get_db),
):
    return approval_service.create_approval_document(
        db,
        request,
    )