from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from ulid import ULID

from turtled_backend.common.util.database import Base


class User(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    username = Column(String(length=100), unique=True, nullable=False)
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


class UserDevice(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    device_token = Column(String(length=255), nullable=False)

    user_id = Column(String(length=255), ForeignKey("tb_user.id"), nullable=True)
    user = relationship("User", backref=backref("UserDevice"))

    @staticmethod
    def of(device_token: str, user_id: str):
        return UserDevice(user_id=user_id, device_token=device_token)

    def update(self, device_token: str, user_id: str):
        self.device_token = device_token
        self.user_id = user_id
