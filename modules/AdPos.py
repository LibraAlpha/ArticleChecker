from sqlalchemy import Column, String, Boolean, Date, Text, BigInteger, VARCHAR, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AdPos(Base):
    __tablename__ = 'adpos'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bid = Column(Integer)
    adv = Column(String)
    impression = Column(Integer)
    click = Column(Integer)
    dt = Column(Date)
    hr = Column(Integer)


class AdPosInfo(Base):
    __tablename__ = 'adpos_info'

    id = Column(Integer)
    name = Column(String, primary_key=True)
