from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

app = FastAPI(
    title="Sentinel API",
    description="Website and API monitoring system",
    version="1.0.0"
)


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