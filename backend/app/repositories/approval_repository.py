from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.approval_document import ApprovalDocument
from app.models.approval_history import ApprovalHistory
from app.models.approval_line import ApprovalLine


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
