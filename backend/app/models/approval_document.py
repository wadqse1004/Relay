from datetime import datetime

from sqlalchemy import BigInteger, Boolean, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ApprovalDocument(Base):
    __tablename__ = "approval_documents"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    document_no: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    document_type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("common_codes.id"),
        nullable=False,
    )

    requester_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    status_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("common_codes.id"),
        nullable=False,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
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