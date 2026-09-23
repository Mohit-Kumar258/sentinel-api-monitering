from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Monitor
from app.schemas.monitor import MonitorCreate, MonitorResponse

from app.utils.auth import get_current_user
from app.models import Monitor, User

router = APIRouter(
    prefix="/monitors",
    tags=["Monitors"]
)


@router.post(
    "",
    response_model=MonitorResponse,
    status_code=201
)
@router.post("", response_model=MonitorResponse, status_code=201)
def create_monitor(
    monitor_data: MonitorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    monitor = Monitor(
        user_id=current_user.id,
        name=monitor_data.name,
        url=str(monitor_data.url),
        interval_seconds=monitor_data.interval_seconds,
        timeout_seconds=monitor_data.timeout_seconds,
        current_status="UNKNOWN"
    )

    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    return monitor

@router.get(
    "",
    response_model=list[MonitorResponse]
)
def get_monitors(
    db: Session = Depends(get_db)
):

    monitors = db.query(Monitor).all()

    return monitors


@router.get(
    "/{monitor_id}",
    response_model=MonitorResponse
)
def get_monitor(
    monitor_id: int,
    db: Session = Depends(get_db)
):

    monitor = (
        db.query(Monitor)
        .filter(Monitor.id == monitor_id)
        .first()
    )

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    return monitor


@router.delete(
    "/{monitor_id}"
)
def delete_monitor(
    monitor_id: int,
    db: Session = Depends(get_db)
):

    monitor = (
        db.query(Monitor)
        .filter(Monitor.id == monitor_id)
        .first()
    )

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    db.delete(monitor)
    db.commit()

    return {
        "message": "Monitor deleted successfully"
    }