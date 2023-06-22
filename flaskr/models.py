from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from flaskr.database import Base
from datetime import datetime
import json
class User(Base):
    __tablename__= 'users'
    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String(10), unique=True)
    password: Mapped[str] = Column(String(8))

class Pc(Base):
    __tablename__= 'pc'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    ipv4: Mapped[str] = mapped_column(String(20))
    created: Mapped[str] = mapped_column(String(15), default=datetime.now().strftime('%Y-%m-%d'))

    ping_history: Mapped[List["Ping"]] = relationship(back_populates="current_pc", cascade="all, delete-orphan")

    def to_json(self):
        pc = {
            "id": self.id,
            "name": self.name,
            "ipv4": self.ipv4,
            "created": self.created
        }
        return json.dumps(pc)
class Ping(Base):
    __tablename__= 'ping'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    current_pc_id: Mapped[int] = mapped_column(ForeignKey("pc.id"))
    created: Mapped[str] = mapped_column(String(15), default=datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
    ipv4_used: Mapped[str] = mapped_column(String(20), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    sent: Mapped[int]  = mapped_column(Integer, nullable=False)
    lost: Mapped[int]  = mapped_column(Integer, nullable=False)
    max_ms: Mapped[str] = mapped_column(String(20), nullable=False)
    min_ms: Mapped[str] = mapped_column(String(20), nullable=False)
    avg_ms: Mapped[str] = mapped_column(String(20), nullable=False)
    
    current_pc: Mapped["Pc"] = relationship(back_populates="ping_history")