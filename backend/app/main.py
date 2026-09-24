from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import User, Monitor, Check, Incident

from app.routes.auth import router as auth_router
from app.routes.monitors import router as monitor_router

from app.services.monitor_checker import check_monitor


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


@app.post("/test-monitor/{monitor_id}")
def test_monitor(
    monitor_id: int,
    db: Session = Depends(get_db)
):
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id
    ).first()

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    check = check_monitor(monitor, db)

    return {
        "monitor_id": monitor.id,
        "monitor_status": monitor.current_status,
        "check_id": check.id,
        "status": check.status,
        "status_code": check.status_code,
        "response_time_ms": check.response_time_ms,
        "error_message": check.error_message
    }