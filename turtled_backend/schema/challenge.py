import datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import backref, relationship
from ulid import ULID

from turtled_backend.common.util.database import Base


class Medal(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    image = Column(String(length=100), nullable=False)
    title = Column(String(length=100), nullable=False)
    subtitle = Column(String(length=500), nullable=False)
    content = Column(String(length=500), nullable=False)
    requirement = Column(String(length=500), nullable=False)
    order = Column(Integer, default=0)


class UserChallenge(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    isAchieved = Column(Boolean, default=False, nullable=False)

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"))
    user = relationship("User", backref=backref("UserChallenge"))

    medal_id = Column(String(length=255), ForeignKey("tb_medal.id", ondelete="SET NULL"))
    medal = relationship("Medal", backref=backref("UserChallenge"))

    @staticmethod
    def of(user_id: str, medal_id: str):
        return UserChallenge(user_id=user_id, medal_id=medal_id)


class CalenderRecordList(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    month_and_year = Column(String(length=15), nullable=False)
    date_field = Column(MutableDict.as_mutable(JSON))

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"), nullable=False)
    user = relationship("User", backref=backref("CalenderList"))

    @staticmethod
    def of(month_and_year: month_and_year, user_id: str, date_field: Optional[dict] = None):
        return CalenderRecordList(month_and_year=month_and_year, user_id=user_id, date_field=date_field)

    def update(self, event_date: str):
        self.date_field[event_date] = True


class ChallengeRecord(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    repeat_cycle = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False, default=0)

    device_id = Column(String(length=255), ForeignKey("tb_user_device.id", ondelete="SET NULL"))
    device = relationship("UserDevice", backref=backref("ChallengeRecord"))

    @staticmethod
    def of(start_time: datetime, repeat_cycle: int, device_id: str):
        return ChallengeRecord(start_time=start_time, repeat_cycle=repeat_cycle, device_id=device_id)

    def update(self, count: int, end_time: datetime):
        self.count = count
        self.end_time = end_time
