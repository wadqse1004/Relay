from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository


def get_users(db: Session) -> list[User]:
    return user_repository.find_all(db)


def get_user(db: Session, user_id: int) -> User:
    user = user_repository.find_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user