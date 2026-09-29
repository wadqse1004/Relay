from fastapi import FastAPI

from app.core.database import check_database_connection
from app.routers.department_router import router as department_router
from app.routers.user_router import router as user_router


app = FastAPI(
    title="Relay API",
    version="0.1.0",
)


app.include_router(department_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "Relay API"
    }


@app.get("/health")
def health():
    db_connected = check_database_connection()

    return {
        "status": "ok" if db_connected else "error",
        "database": "connected" if db_connected else "disconnected",
    }