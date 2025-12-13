
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class MessageRequestSchema(BaseModel):
    message: str
    session_id: Optional[str] = None

    @field_validator('message')
    def validate_message(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Please enter a valid message')

        return v


class MessageResponseSchema(BaseModel):
    message: str
    session_id: str
    timestamp: datetime

