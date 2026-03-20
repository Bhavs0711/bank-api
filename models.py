from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    ifsc = Column(String, unique=True, index=True)
    branch = Column(String)
    address = Column(String)
    city = Column(String)
    district = Column(String)
    state = Column(String)
    bank_id = Column(Integer, ForeignKey("banks.id"))