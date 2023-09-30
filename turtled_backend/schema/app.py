from __future__ import annotations

from sqlalchemy import Column, String
from ulid import ULID

from turtled_backend.common.util.database import Base


class App(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    version = Column(String(length=100))
