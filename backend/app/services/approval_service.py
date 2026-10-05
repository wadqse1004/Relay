from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.approval_document import ApprovalDocument
from app.models.approval_history import ApprovalHistory
from app.models.approval_line import ApprovalLine
from app.repositories import approval_repository
from app.schemas.approval import ApprovalDocumentCreate


def create_approval_document(
    db: Session,
    request: ApprovalDocumentCreate,
) -> ApprovalDocument:
    try:
        pending_status_id = approval_repository.find_common_code_id(
            db,
            "APPROVAL_STATUS",
            "PENDING",
        )

        waiting_line_status_id = approval_repository.find_common_code_id(
            db,
            "APPROVAL_LINE_STATUS",
            "WAITING",
        )

        submit_action_id = approval_repository.find_common_code_id(
            db,
            "APPROVAL_ACTION",
            "SUBMIT",
        )

        if (
            pending_status_id is None
            or waiting_line_status_id is None
            or submit_action_id is None
        ):
            raise HTTPException(
                status_code=500,
                detail="Approval common code not found",
            )

        document_no = f"APV-{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}"

        document = ApprovalDocument(
            document_no=document_no,
            document_type_id=request.document_type_id,
            requester_id=request.requester_id,
            title=request.title,
            status_id=pending_status_id,
            submitted_at=datetime.now(),
            created_by=request.requester_id,
            updated_by=request.requester_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        approval_repository.add_document(db, document)

        for approver in request.approvers:
            line = ApprovalLine(
                approval_document_id=document.id,
                approver_id=approver.approver_id,
                sequence=approver.sequence,
                status_id=waiting_line_status_id,
                created_by=request.requester_id,
                updated_by=request.requester_id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            approval_repository.add_line(db, line)

        history = ApprovalHistory(
            approval_document_id=document.id,
            approval_line_id=None,
            actor_id=request.requester_id,
            action_id=submit_action_id,
            comment="결재문서 상신",
            created_at=datetime.now(),
        )

        approval_repository.add_history(db, history)

        db.commit()
        db.refresh(document)

        return document

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        print("CREATE APPROVAL ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )