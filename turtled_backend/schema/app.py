from __future__ import annotations

from ulid import ULID

from sqlalchemy import Column, String

from turtled_backend.common.util.database import Base


class App(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    update_version = Column(String(length=100))
