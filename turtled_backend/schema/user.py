from __future__ import annotations

from ulid import ULID

from sqlalchemy import Column, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import backref, relationship

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
    update_version_id = Column(String(length=255), ForeignKey("tb_medal.id", ondelete="SET NULL"))
    update_version = relationship("App", backref=backref("User"))


class UserDevice(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    device_token = Column(String(length=255), nullable=False)
    device_info = Column(JSON(), nullable=True)

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"))
    user = relationship("User", backref=backref("CalenderDateRecord"))
