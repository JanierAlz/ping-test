from sqlalchemy import Column, Integer, String, Boolean
from flaskr.database import Base
from datetime import datetime

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True)
    password = Column(String(8))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

class Pc(Base):
    __tablename__= 'pc'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    ipv4 = Column(String(20))
    disabled = Column(Boolean, default=False)
    created = Column(String(15), default=datetime.now().strftime('%Y-%m-%d'))
    def __init__(self, name=None, ipv4=None):
        self.name = name
        self.ipv4 = ipv4

class Ping(Base):
    __tablename__= 'ping'
    id = Column(Integer, primary_key=True)
    pc_id = Column(Integer, nullable=False)
    created = Column(String(15), default=datetime.now().strftime('%Y-%m-%d'))
    success = Column(Boolean, nullable=False)
    sent = Column(Integer, nullable=False)
    lost = Column(Integer, nullable=False)
    max_ms = Column(String(20), nullable=False)
    min_ms = Column(String(20), nullable=False)
    avg_ms = Column(String(20), nullable=False)

    
    def __init__(self, pc_id=None, success=None, sent=None, lost=None, max_ms=None, min_ms=None, avg_ms=None):
        self.pc_id = pc_id
        self.success = success
        self.sent = sent
        self.lost = lost
        self.max_ms = max_ms
        self.min_ms = min_ms
        self.avg_ms = avg_ms