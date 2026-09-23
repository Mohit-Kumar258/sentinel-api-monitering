from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base

from app.models import (
    User,
    Monitor,
    Check,
    Incident
)

from app.routes.auth import router as auth_router
from app.routes.monitors import router as monitor_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sentinel API",
    description="Website and API monitoring system",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(monitor_router)


@app.get("/")
def root():
    return {
        "message": "Sentinel API is running"
    }


@app.get("/test-db")
def test_db():

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            value = result.scalar()

        return {
            "database": "connected",
            "result": value
        }

    except Exception as e:

        return {
            "database": "connection failed",
            "error": str(e)
        }