from database import SessionLocal
from models import CallLog
from datetime import datetime

def update_status(call_sid, status):

    db = SessionLocal()

    call = db.query(CallLog).filter(
        CallLog.call_sid == call_sid
    ).first()

    if call:
        call.status = status
        db.commit()

    db.close()

def create_call(call_sid, customer_name, phone_number, policy_number):
    db = SessionLocal()

    call = CallLog(
        call_sid=call_sid,
        customer_name=customer_name,
        phone_number=phone_number,
        policy_number=policy_number,
        status="Started",
        start_time=datetime.utcnow()
    )

    db.add(call)
    db.commit()
    db.close()


def update_call(call_sid, status, transcript, summary):
    db = SessionLocal()

    call = db.query(CallLog).filter(CallLog.call_sid == call_sid).first()

    if call:
        call.status = status
        call.transcript = transcript
        call.summary = summary
        call.end_time = datetime.utcnow()

        if call.start_time:
            duration = call.end_time - call.start_time
            call.duration = int(duration.total_seconds())

        db.commit()

    db.close()