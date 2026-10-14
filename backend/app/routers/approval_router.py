from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.approval import (
    ApprovalDocumentCreate,
    ApprovalDocumentResponse,
)
from app.services import approval_service
from app.services.approval_service import (
    approve_document,
    reject_document,
    get_approval_inbox,
)
from app.schemas.approval import (
    ApprovalActionRequest,
    ApprovalDocumentResponse,
    ApprovalInboxItemResponse,
)


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

@router.post(
    "/{document_id}/approve",
    response_model=ApprovalDocumentResponse,
)
def approve(
    document_id: int,
    request: ApprovalActionRequest,
    db: Session = Depends(get_db),
):
    return approve_document(
        db=db,
        document_id=document_id,
        request=request,
    )


@router.post(
    "/{document_id}/reject",
    response_model=ApprovalDocumentResponse,
)
def reject(
    document_id: int,
    request: ApprovalActionRequest,
    db: Session = Depends(get_db),
):
    return reject_document(
        db=db,
        document_id=document_id,
        request=request,
    )

@router.get(
    "/inbox",
    response_model=list[ApprovalInboxItemResponse],
)
def get_inbox(
    approver_id: int,
    db: Session = Depends(get_db),
):
    return get_approval_inbox(
        db=db,
        approver_id=approver_id,
    )