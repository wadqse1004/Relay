from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.department import Department


def find_all(db: Session) -> list[Department]:
    statement = (
        select(Department)
        .order_by(Department.sort_order, Department.id)
    )

    return list(db.scalars(statement).all())