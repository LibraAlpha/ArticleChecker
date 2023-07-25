from sqlalchemy import Column, String, Boolean, Date, Text, BigInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Asset(Base):
    __tablename__ = 'assets'

    id = Column(BigInteger, primary_key=True)
    title = Column(String)
    asset_desc = Column(String)
    url = Column(Text)
    is_sensitive = Column(Boolean)
    is_checked = Column(Boolean)
    adv = Column(String)
    sensitive_words = Column(String)
    reason = Column(String)
    ad_pos = Column(String)
    created_at = Column(String)

