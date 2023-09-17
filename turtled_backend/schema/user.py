from sqlalchemy import Column, Integer, String

from turtled_backend.common.util.database import Base


class UserLoginInfo(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=100))
    password = Column(String(length=100))

