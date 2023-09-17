from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Column, String

from turtled_backend.common.util.database import Base


class User(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(length=100))
    email = Column(String(length=100))
    password = Column(String(length=100))
    deviceToken = Column(String(length=100))
    disabled: bool | None = None
