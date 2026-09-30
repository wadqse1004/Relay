from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories import user_repository
from app.schemas.auth import LoginRequest


def login(
    db: Session,
    request: LoginRequest,
) -> str:
    user = user_repository.find_by_email(
        db,
        request.email,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return create_access_token(
        subject=str(user.id)
    )