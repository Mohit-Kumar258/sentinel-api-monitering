from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

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

    started_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    duration_seconds = Column(
        Integer,
        nullable=True
    )

    reason = Column(
        String(500),
        nullable=True
    )