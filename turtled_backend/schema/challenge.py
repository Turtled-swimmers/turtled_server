from uuid import uuid4

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from turtled_backend.common.util.database import Base


class Medal(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()))
    image = Column(String(length=100))
    title = Column(String(length=100))
    subtitle = Column(String(length=100))
    content = Column(String(length=100))
    requirement = Column(String(length=100))


class UserChallenge(Base):
    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()))
    isAchieved = Column(Boolean, default=False, nullable=False)

    user_id = Column(String(length=255), ForeignKey("tb_user.id", ondelete="SET NULL"))
    user = relationship("User", backref=backref("Center"))

    medal_id = Column(String(length=255), ForeignKey("tb_medal.id", ondelete="SET NULL"))
    medal = relationship("User", backref=backref("Center"))
