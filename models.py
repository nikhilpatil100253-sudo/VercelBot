from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class CallLog(Base):

    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True)

    call_sid = Column(String(100), unique=True)

    customer_name = Column(String(100))

    phone_number = Column(String(20))

    policy_number = Column(String(50))

    status = Column(String(50))

    start_time = Column(DateTime, default=datetime.utcnow)

    end_time = Column(DateTime)

    duration = Column(Integer)

    transcript = Column(Text)

    summary = Column(Text)
    