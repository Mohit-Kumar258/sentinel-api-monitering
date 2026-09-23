from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class Check(Base):
    __tablename__ = "checks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    monitor_id = Column(
        Integer,
        ForeignKey("monitors.id"),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False
    )

    status_code = Column(
        Integer,
        nullable=True
    )

    response_time_ms = Column(
        Float,
        nullable=True
    )

    error_message = Column(
        String(500),
        nullable=True
    )

    checked_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )