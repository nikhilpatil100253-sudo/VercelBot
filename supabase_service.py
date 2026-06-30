import os
from datetime import datetime, timezone

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_call(call_sid, customer_name, phone_number, policy_number):

    supabase.table("call_logs").insert({

        "call_sid": call_sid,

        "customer_name": customer_name,

        "phone_number": phone_number,

        "policy_number": policy_number,

        "status": "Started",

        "start_time": datetime.now(timezone.utc).isoformat()

    }).execute()


def update_call(
    call_sid,
    status,
    transcript,
    summary,
    sentiment,
    customer_interest,
    call_outcome,
    follow_up_required,
    follow_up_reason,
    ai_summary
):

    data = {

        "status": status,

        "transcript": transcript,

        "summary": summary,

        "sentiment": sentiment,

        "customer_interest": customer_interest,

        "call_outcome": call_outcome,

        "follow_up_required": follow_up_required,

        "follow_up_reason": follow_up_reason,

        "ai_summary": ai_summary,

        "end_time": datetime.now(timezone.utc).isoformat()

    }

    supabase.table("call_logs") \
        .update(data) \
        .eq("call_sid", call_sid) \
        .execute()

def update_status(call_sid, status):

    supabase.table("call_logs") \
        .update({

            "status": status

        }) \
        .eq("call_sid", call_sid) \
        .execute()

def get_calls():

    response = supabase.table("call_logs").select("*").execute()

    return response.data