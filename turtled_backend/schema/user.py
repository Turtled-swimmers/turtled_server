from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from ulid import ULID

from turtled_backend.common.util.database import Base


class User(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    username = Column(String(length=100), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=100), nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)

    medal_id = Column(String(length=255), ForeignKey("tb_medal.id", ondelete="SET NULL"))
    medal = relationship("Medal", backref=backref("User"))

    is_notification_active = Column(Boolean, default=False)

    @staticmethod
    def of(username: str, email: str, password: str):
        return User(
            username=username,
            email=email,
            password=password,
        )

    def update(self, medal_id: str):
        self.medal_id = medal_id


class UserDevice(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    device_token = Column(String(length=255), nullable=False)

    user_id = Column(String(length=255), ForeignKey("tb_user.id"), nullable=True)
    user = relationship("User", backref=backref("UserDevice"))

    @staticmethod
    def of(device_token: str, user_id: Optional[str] = None):
        return UserDevice(user_id=user_id, device_token=device_token)

    def update(self, device_token: str, user_id: Optional[str] = None):
        self.device_token = device_token
        self.user_id = user_id
