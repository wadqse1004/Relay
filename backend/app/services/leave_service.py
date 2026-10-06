from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.approval_document import ApprovalDocument
from app.models.approval_history import ApprovalHistory
from app.models.approval_line import ApprovalLine
from app.models.leave_request import LeaveRequest
from app.repositories.approval_repository import (
    add_document,
    add_history,
    add_line,
    find_common_code_id,
)
from app.repositories.leave_repository import (
    add_leave_request,
    find_leave_balance,
)
from app.schemas.leave import LeaveRequestCreate


def create_leave_request(
    db: Session,
    request: LeaveRequestCreate,
) -> LeaveRequest:
    try:
        # 1. 연차 잔액 조회
        balance = find_leave_balance(
            db=db,
            user_id=request.user_id,
            year=request.start_date.year,
        )

        if balance is None:
            raise HTTPException(
                status_code=400,
                detail="연차 잔액 정보가 없습니다.",
            )

        # 2. 잔여 연차 검증
        if balance.remaining_days < request.days:
            raise HTTPException(
                status_code=400,
                detail="잔여 연차가 부족합니다.",
            )

        # 3. 공통 코드 조회
        pending_status_id = find_common_code_id(
            db,
            "APPROVAL_STATUS",
            "PENDING",
        )

        waiting_status_id = find_common_code_id(
            db,
            "APPROVAL_LINE_STATUS",
            "WAITING",
        )

        submit_action_id = find_common_code_id(
            db,
            "APPROVAL_ACTION",
            "SUBMIT",
        )

        leave_document_type_id = find_common_code_id(
            db,
            "APPROVAL_DOCUMENT_TYPE",
            "LEAVE",
        )

        # 4. 결재 문서 생성
        now = datetime.now()

        document = ApprovalDocument(
            document_no=f"LEAVE-{now.strftime('%Y%m%d%H%M%S')}",
            document_type_id=leave_document_type_id,
            requester_id=request.user_id,
            title=f"{request.start_date} 휴가 신청",
            status_id=pending_status_id,
            submitted_at=now,
            completed_at=None,
            is_active=True,
            created_by=request.user_id,
            created_at=now,
            updated_by=request.user_id,
            updated_at=now,
        )

        add_document(db, document)

        # 5. 결재선 생성
        for index, approver_id in enumerate(
            request.approver_ids,
            start=1,
        ):
            line = ApprovalLine(
                approval_document_id=document.id,
                approver_id=approver_id,
                sequence=index,
                status_id=waiting_status_id,
                acted_at=None,
                comment=None,
                is_active=True,
                created_by=request.user_id,
                created_at=now,
                updated_by=request.user_id,
                updated_at=now,
            )

            add_line(db, line)

        # 6. 상신 이력 생성
        history = ApprovalHistory(
            approval_document_id=document.id,
            approval_line_id=None,
            actor_id=request.user_id,
            action_id=submit_action_id,
            comment="휴가 신청 상신",
            created_at=now,
        )

        add_history(db, history)

        # 7. 연차 신청 생성
        leave_request = LeaveRequest(
            approval_document_id=document.id,
            user_id=request.user_id,
            leave_type_id=request.leave_type_id,
            start_date=request.start_date,
            end_date=request.end_date,
            days=request.days,
            reason=request.reason,
            is_active=True,
            created_by=request.user_id,
            created_at=now,
            updated_by=request.user_id,
            updated_at=now,
        )

        add_leave_request(db, leave_request)

        # 8. 전체 성공 시 commit
        db.commit()
        db.refresh(leave_request)

        return leave_request

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("CREATE LEAVE REQUEST ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="휴가 신청 처리 중 오류가 발생했습니다.",
        )