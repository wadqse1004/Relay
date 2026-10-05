from datetime import datetime

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ApprovalLine(Base):
    __tablename__ = "approval_lines"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    approval_document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("approval_documents.id"),
        nullable=False,
    )

    approver_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("common_codes.id"),
        nullable=False,
    )

    acted_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
    )

    updated_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
    )