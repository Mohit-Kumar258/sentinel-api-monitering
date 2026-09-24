from pydantic import BaseModel, HttpUrl, Field


class MonitorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    url: HttpUrl
    interval_seconds: int = Field(default=30, ge=10)
    timeout_seconds: int = Field(default=10, ge=1)

class MonitorUpdate(BaseModel):
    name: str | None = None
    url: HttpUrl | None = None
    interval_seconds: int | None = Field(default=None, ge=10)
    timeout_seconds: int | None = Field(default=None, ge=1)
class MonitorResponse(BaseModel):
    id: int
    name: str
    url: str
    interval_seconds: int
    timeout_seconds: int
    is_active: bool
    current_status: str

    class Config:
        from_attributes = True