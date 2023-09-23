from ulid import ULID

from sqlalchemy import Boolean, Column, ForeignKey, String, JSON, Date, Integer, DateTime
from sqlalchemy.orm import backref, relationship

from turtled_backend.common.util.database import Base


class Medal(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    image = Column(String(length=100))
    title = Column(String(length=100))
    subtitle = Column(String(length=100))
    content = Column(String(length=100))
    requirement = Column(String(length=100))


class UserChallenge(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    isAchieved = Column(Boolean, default=False, nullable=False)

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"))
    user = relationship("User", backref=backref("Center"))

    medal_id = Column(String(length=255), ForeignKey("tb_medal.id", ondelete="SET NULL"))
    medal = relationship("User", backref=backref("Center"))


class UserUpdateHistory(Base): # to do : does this model needed?
    id = Column(String(length=255), primary_key=True, default=lambda: str(ULID()))
    initial_update_date = Column(Date, nullable=False)
    last_update_date = Column(Date)


class CalenderList(Base):
    month_and_year = Column(String(length=15), nullable=False)
    date_field = Column(JSON())

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"))
    user = relationship("User", backref=backref("Center"))


class CalenderDateRecord(Base):
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    repeat_time = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"))
    user = relationship("User", backref=backref("Center"))
