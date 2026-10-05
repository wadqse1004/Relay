from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ApprovalHistory(Base):
    __tablename__ = "approval_histories"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    approval_document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("approval_documents.id"),
        nullable=False,
    )

    approval_line_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("approval_lines.id"),
        nullable=True,
    )

    actor_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
    )

    action_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("common_codes.id"),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
    )