from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def find_all(db: Session) -> list[User]:
    statement = select(User).order_by(User.id)

    return list(db.scalars(statement).all())


def find_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)