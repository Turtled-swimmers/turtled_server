from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from ulid import ULID

from turtled_backend.common.util.database import Base


class User(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    username = Column(String(length=100))
    email = Column(String(length=100))
    password = Column(String(length=100))
    disabled = Column(Boolean, default=False, nullable=False)

    medal_id = Column(String(length=255), ForeignKey("tb_medal.id", ondelete="SET NULL"))
    medal = relationship("Medal", backref=backref("User"))

    is_notification_active = Column(Boolean, default=False, nullable=False)


class UserDevice(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    device_token = Column(String(length=255), nullable=False)
    device_uuid = Column(String(length=255), nullable=True)

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="CASCADE"))
    user = relationship("User", backref=backref("UserDevice"))

    def update(self, device_token: str):
        self.device_token = device_token
