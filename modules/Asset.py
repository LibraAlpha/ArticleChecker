from sqlalchemy import Column, String, Boolean, Date, Text, BigInteger, VARCHAR, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Asset(Base):
    __tablename__ = 'assets'

    id = Column(BigInteger, primary_key=True)
    title = Column(String)
    asset_desc = Column(String)
    url = Column(Text)
    url_md5 = Column(String)
    is_sensitive = Column(Boolean)
    is_checked = Column(Boolean)
    adv = Column(String)
    sensitive_words = Column(String)
    reason = Column(String)
    ad_pos = Column(String)
    created_at = Column(String)
    bid = Column(Integer)
    impression = Column(Integer)
    click = Column(Integer)
    url_replaced = Column(String)
    url_replaced_md5 = Column(String)
    video_url = Column(String)
    video_url_md5 = Column(String)
    logo_url = Column(String)
