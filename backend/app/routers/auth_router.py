from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)
from app.services import auth_service


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    access_token = auth_service.login(
        db,
        request,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }