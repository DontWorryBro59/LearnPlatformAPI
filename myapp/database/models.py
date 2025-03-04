from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

class OrmUser(Base):
    __tablename__ = "users"

    id : Mapped[int] = Column(Integer, primary_key=True)
    first_name : Mapped[str] = Column(String)
    second_name : Mapped[str] = Column(String)
    email : Mapped[str] = Column(String)
    age : Mapped[int] = Column(Integer)
