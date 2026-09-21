from fastapi import FastAPI

from app.core.database import check_database_connection


app = FastAPI(
    title="Relay API",
    version="0.1.0",
)


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