from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.department import DepartmentResponse
from app.services import department_service


router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"],
)


@router.get("", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
):
    return department_service.get_departments(db)