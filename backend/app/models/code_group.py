from datetime import datetime

from sqlalchemy import BigInteger, Boolean, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CodeGroup(Base):
    __tablename__ = "code_groups"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_by: Mapped[int | None] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    updated_by: Mapped[int | None] = mapped_column(BigInteger)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)