from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IdempotencyKeyCreateDTO(BaseModel):
    key: str
    scope: str
    response_json: Optional[str] = None
    expires_at: datetime


class IdempotencyKeyResponseDTO(BaseModel):
    key: str
    scope: str
    response_json: Optional[str] = None
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


class OutboxEventCreateDTO(BaseModel):
    aggregate_type: str
    aggregate_id: int
    event_type: str
    payload_json: str


class OutboxEventResponseDTO(BaseModel):
    event_id: int
    aggregate_type: str
    aggregate_id: int
    event_type: str
    payload_json: str
    status: str
    created_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OutboxEventUpdateDTO(BaseModel):
    status: str
    sent_at: Optional[datetime] = None
