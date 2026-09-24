from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Monitor, User
from app.schemas.monitor import (
    MonitorCreate,
    MonitorUpdate,
    MonitorResponse
)
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/monitors",
    tags=["Monitors"]
)


@router.post(
    "",
    response_model=MonitorResponse,
    status_code=201
)
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    monitors = db.query(Monitor).filter(
        Monitor.user_id == current_user.id
    ).all()

    return monitors

@router.put(
    "/{monitor_id}",
    response_model=MonitorResponse
)
def update_monitor(
    monitor_id: int,
    monitor_data: MonitorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    if monitor_data.name is not None:
        monitor.name = monitor_data.name

    if monitor_data.url is not None:
        monitor.url = str(monitor_data.url)

    if monitor_data.interval_seconds is not None:
        monitor.interval_seconds = monitor_data.interval_seconds

    if monitor_data.timeout_seconds is not None:
        monitor.timeout_seconds = monitor_data.timeout_seconds

    db.commit()
    db.refresh(monitor)

    return monitor
@router.get(
    "/{monitor_id}",
    response_model=MonitorResponse
)
def get_monitor(
    monitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()

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