from sqlalchemy.orm import Session

from app.models.department import Department
from app.repositories import department_repository


def get_departments(db: Session) -> list[Department]:
    return department_repository.find_all(db)