import datetime
from sqlalchemy import Column, DateTime, Integer, String
from .database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(32), unique=True, index=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    clicks = Column(Integer, default=0)

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(32), index=True, nullable=False)
    accessed_at = Column(DateTime, default=datetime.datetime.utcnow)
    client_ip = Column(String(64), nullable=True)
    user_agent = Column(String(512), nullable=True)
