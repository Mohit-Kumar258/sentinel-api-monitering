import time
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.models import Monitor, Check, Incident


def check_monitor(
    monitor: Monitor,
    db: Session
):
    start_time = time.perf_counter()

    try:
        response = httpx.get(
            monitor.url,
            timeout=monitor.timeout_seconds,
            follow_redirects=True
        )

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000

        if 200 <= response.status_code < 400:
            status = "UP"
        else:
            status = "DOWN"

        error_message = None

    except httpx.TimeoutException:

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000

        status = "DOWN"
        response = None
        error_message = "Request timed out"

    except httpx.RequestError as e:

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000

        status = "DOWN"
        response = None
        error_message = str(e)[:500]

    # --------------------------------
    # Save check
    # --------------------------------

    check = Check(
        monitor_id=monitor.id,
        status=status,
        status_code=response.status_code if response else None,
        response_time_ms=elapsed_ms,
        error_message=error_message
    )

    db.add(check)

    # --------------------------------
    # Handle incidents
    # --------------------------------

    previous_status = monitor.current_status

    if status == "DOWN" and previous_status != "DOWN":

        incident = Incident(
            monitor_id=monitor.id,
            started_at=datetime.now(timezone.utc),
            reason=error_message or f"HTTP {response.status_code}"
        )

        db.add(incident)

    elif status == "UP" and previous_status == "DOWN":

        incident = (
            db.query(Incident)
            .filter(
                Incident.monitor_id == monitor.id,
                Incident.resolved_at.is_(None)
            )
            .order_by(Incident.started_at.desc())
            .first()
        )

        if incident:

            resolved_at = datetime.now(timezone.utc)

            incident.resolved_at = resolved_at

            incident.duration_seconds = int(
                (
                    resolved_at - incident.started_at
                ).total_seconds()
            )

    # --------------------------------
    # Update monitor status
    # --------------------------------

    monitor.current_status = status

    db.commit()
    db.refresh(check)

    return check