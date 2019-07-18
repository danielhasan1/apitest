from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT
from database import Base


class pin(Base):
    __tablename__ = "pincode"
    id = Column(Integer, primary_key=True)
    loc = Column(String)
    address = Column(String)
    city = Column(String)
    lat = Column(DOUBLE_PRECISION)
    lon = Column(DOUBLE_PRECISION)
    accuracy = Column(String)
class pol(Base):
    __tablename__ = "poly"
    name = Column(String,primary_key=True)
    parent = Column(String)
    cord = Column(TEXT)

