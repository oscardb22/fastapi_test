import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    is_active: bool = Field(default=True)
    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(default=datetime.now(UTC))
