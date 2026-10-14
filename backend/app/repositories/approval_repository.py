from sqlalchemy.orm import aliased, Session
from sqlalchemy import exists, select, text

from app.models.approval_document import ApprovalDocument
from app.models.approval_history import ApprovalHistory
from app.models.approval_line import ApprovalLine
from app.models.common_code import CommonCode
from app.models.user import User
from app.models.leave_request import LeaveRequest


def find_common_code_id(
    db: Session,
    group_code: str,
    code: str,
) -> int | None:
    statement = text("""
        SELECT cc.id
        FROM common_codes cc
        JOIN code_groups cg
          ON cg.id = cc.group_id
        WHERE cg.code = :group_code
          AND cc.code = :code
          AND cc.is_active = TRUE
        LIMIT 1
    """)

    return db.scalar(
        statement,
        {
            "group_code": group_code,
            "code": code,
        },
    )


def add_document(
    db: Session,
    document: ApprovalDocument,
) -> ApprovalDocument:
    db.add(document)

    # INSERT를 DB로 보내서 document.id를 받아옴
    # 하지만 아직 COMMIT은 하지 않음
    db.flush()

    return document


def add_line(
    db: Session,
    line: ApprovalLine,
) -> ApprovalLine:
    db.add(line)
    db.flush()

    return line


def add_history(
    db: Session,
    history: ApprovalHistory,
) -> ApprovalHistory:
    db.add(history)
    db.flush()

    return history

def find_document(
    db: Session,
    document_id: int,
) -> ApprovalDocument | None:
    return db.get(ApprovalDocument, document_id)


def find_approval_line(
    db: Session,
    document_id: int,
    approver_id: int,
) -> ApprovalLine | None:
    stmt = (
        select(ApprovalLine)
        .where(
            ApprovalLine.approval_document_id == document_id,
            ApprovalLine.approver_id == approver_id,
            ApprovalLine.is_active.is_(True),
        )
    )

    return db.scalar(stmt)


def find_remaining_waiting_lines(
    db: Session,
    document_id: int,
    waiting_status_id: int,
) -> list[ApprovalLine]:
    stmt = (
        select(ApprovalLine)
        .where(
            ApprovalLine.approval_document_id == document_id,
            ApprovalLine.status_id == waiting_status_id,
            ApprovalLine.is_active.is_(True),
        )
        .order_by(ApprovalLine.sequence)
    )

    return list(db.scalars(stmt))

def find_previous_waiting_line(
    db: Session,
    document_id: int,
    current_sequence: int,
    waiting_status_id: int,
) -> ApprovalLine | None:
    stmt = (
        select(ApprovalLine)
        .where(
            ApprovalLine.approval_document_id == document_id,
            ApprovalLine.sequence < current_sequence,
            ApprovalLine.status_id == waiting_status_id,
            ApprovalLine.is_active.is_(True),
        )
        .order_by(ApprovalLine.sequence)
    )

    return db.scalar(stmt)

def find_inbox_documents(
    db: Session,
    approver_id: int,
    waiting_status_id: int,
):
    previous_line = aliased(ApprovalLine)
    leave_type_code = aliased(CommonCode)

    previous_waiting_exists = (
        select(previous_line.id)
        .where(
            previous_line.approval_document_id
            == ApprovalLine.approval_document_id,
            previous_line.sequence
            < ApprovalLine.sequence,
            previous_line.status_id
            == waiting_status_id,
            previous_line.is_active.is_(True),
        )
        .exists()
    )

    stmt = (
        select(
            ApprovalDocument,
            ApprovalLine,
            CommonCode.code.label("document_status_code"),
            CommonCode.name.label("document_status_name"),
            User.name.label("requester_name"),

            leave_type_code.name.label("leave_type_name"),
            LeaveRequest.start_date,
            LeaveRequest.end_date,
            LeaveRequest.days,
            LeaveRequest.reason,
        )
        .join(
            ApprovalLine,
            ApprovalLine.approval_document_id
            == ApprovalDocument.id,
        )
        .join(
            CommonCode,
            CommonCode.id
            == ApprovalDocument.status_id,
        )
        .join(
            User,
            User.id == ApprovalDocument.requester_id,
        )
        .where(
            ApprovalLine.approver_id == approver_id,
            ApprovalLine.status_id == waiting_status_id,
            ApprovalLine.is_active.is_(True),
            ApprovalDocument.is_active.is_(True),
            ~previous_waiting_exists,
        )
        .order_by(
            ApprovalDocument.submitted_at.desc()
        )
        .outerjoin(
            LeaveRequest,
            LeaveRequest.approval_document_id
            == ApprovalDocument.id,
        )
        .outerjoin(
            leave_type_code,
            leave_type_code.id
            == LeaveRequest.leave_type_id,
        )
    )

    return db.execute(stmt).all()