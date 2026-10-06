from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.approval_document import ApprovalDocument
from app.models.approval_history import ApprovalHistory
from app.models.approval_line import ApprovalLine
from app.repositories import approval_repository
from app.schemas.approval import ApprovalDocumentCreate

from app.models.approval_history import ApprovalHistory
from app.repositories.approval_repository import (
    add_history,
    find_approval_line,
    find_common_code_id,
    find_document,
    find_previous_waiting_line,
    find_remaining_waiting_lines,
)
from app.schemas.approval import ApprovalActionRequest
from app.repositories.leave_repository import (
    find_leave_balance,
    find_leave_request_by_document_id,
)


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

def approve_document(
    db: Session,
    document_id: int,
    request: ApprovalActionRequest,
):
    try:
        document = find_document(db, document_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="결재문서를 찾을 수 없습니다.",
            )

        line = find_approval_line(
            db=db,
            document_id=document_id,
            approver_id=request.approver_id,
        )

        if line is None:
            raise HTTPException(
                status_code=404,
                detail="결재선을 찾을 수 없습니다.",
            )

        waiting_status_id = find_common_code_id(
            db,
            "APPROVAL_LINE_STATUS",
            "WAITING",
        )

        approved_line_status_id = find_common_code_id(
            db,
            "APPROVAL_LINE_STATUS",
            "APPROVED",
        )

        approved_document_status_id = find_common_code_id(
            db,
            "APPROVAL_STATUS",
            "APPROVED",
        )

        approve_action_id = find_common_code_id(
            db,
            "APPROVAL_ACTION",
            "APPROVE",
        )

        if line.status_id != waiting_status_id:
            raise HTTPException(
                status_code=400,
                detail="이미 처리된 결재선입니다.",
            )

        previous_waiting_line = find_previous_waiting_line(
            db=db,
            document_id=document_id,
            current_sequence=line.sequence,
            waiting_status_id=waiting_status_id,
        )

        if previous_waiting_line is not None:
            raise HTTPException(
                status_code=400,
                detail="이전 결재자가 아직 처리하지 않았습니다.",
            )

        now = datetime.now()

        line.status_id = approved_line_status_id
        line.acted_at = now
        line.comment = request.comment
        line.updated_by = request.approver_id
        line.updated_at = now

        history = ApprovalHistory(
            approval_document_id=document.id,
            approval_line_id=line.id,
            actor_id=request.approver_id,
            action_id=approve_action_id,
            comment=request.comment,
            created_at=now,
        )

        add_history(db, history)

        db.flush()

        remaining_lines = find_remaining_waiting_lines(
            db=db,
            document_id=document_id,
            waiting_status_id=waiting_status_id,
        )

        if not remaining_lines:
            document.status_id = approved_document_status_id
            document.completed_at = now
            document.updated_by = request.approver_id
            document.updated_at = now

            leave_request = find_leave_request_by_document_id(
                db=db,
                document_id=document_id,
            )

            if leave_request is not None:
                balance = find_leave_balance(
                    db=db,
                    user_id=leave_request.user_id,
                    year=leave_request.start_date.year,
                )

            if balance is None:
                raise HTTPException(
                    status_code=400,
                    detail="연차 잔액 정보를 찾을 수 없습니다.",
                )

            if balance.remaining_days < leave_request.days:
                raise HTTPException(
                    status_code=400,
                    detail="잔여 연차가 부족합니다.",
                )

            balance.used_days += leave_request.days
            balance.remaining_days -= leave_request.days
            balance.updated_by = request.approver_id
            balance.updated_at = now

        db.commit()
        db.refresh(document)

        return document

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("APPROVE ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="결재 승인 처리 중 오류가 발생했습니다.",
        )

def reject_document(
    db: Session,
    document_id: int,
    request: ApprovalActionRequest,
):
    try:
        document = find_document(db, document_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="결재문서를 찾을 수 없습니다.",
            )

        line = find_approval_line(
            db=db,
            document_id=document_id,
            approver_id=request.approver_id,
        )

        if line is None:
            raise HTTPException(
                status_code=404,
                detail="결재선을 찾을 수 없습니다.",
            )

        waiting_status_id = find_common_code_id(
            db,
            "APPROVAL_LINE_STATUS",
            "WAITING",
        )

        rejected_line_status_id = find_common_code_id(
            db,
            "APPROVAL_LINE_STATUS",
            "REJECTED",
        )

        rejected_document_status_id = find_common_code_id(
            db,
            "APPROVAL_STATUS",
            "REJECTED",
        )

        reject_action_id = find_common_code_id(
            db,
            "APPROVAL_ACTION",
            "REJECT",
        )

        if line.status_id != waiting_status_id:
            raise HTTPException(
                status_code=400,
                detail="이미 처리된 결재선입니다.",
            )

        now = datetime.now()

        line.status_id = rejected_line_status_id
        line.acted_at = now
        line.comment = request.comment
        line.updated_by = request.approver_id
        line.updated_at = now

        document.status_id = rejected_document_status_id
        document.completed_at = now
        document.updated_by = request.approver_id
        document.updated_at = now

        history = ApprovalHistory(
            approval_document_id=document.id,
            approval_line_id=line.id,
            actor_id=request.approver_id,
            action_id=reject_action_id,
            comment=request.comment,
            created_at=now,
        )

        add_history(db, history)

        db.commit()
        db.refresh(document)

        return document

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("REJECT ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="결재 반려 처리 중 오류가 발생했습니다.",
        )

