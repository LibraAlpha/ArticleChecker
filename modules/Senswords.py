from sqlalchemy import Column, String, Boolean, Date, Text, BigInteger, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensWord(Base):
    __tablename__ = 'sensitive_words'

    id = Column(BigInteger, primary_key=True)
    sensitive_word = Column(String)
    updated_at = Column(TIMESTAMP)
