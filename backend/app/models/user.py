from datetime import date

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    employee_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    birth_date: Mapped[date | None] = mapped_column(Date)

    department_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id"),
    )

    manager_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
    )

    position_id: Mapped[int | None] = mapped_column(BigInteger)
    job_title_id: Mapped[int | None] = mapped_column(BigInteger)
    status_id: Mapped[int | None] = mapped_column(BigInteger)

    join_date: Mapped[date | None] = mapped_column(Date)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)