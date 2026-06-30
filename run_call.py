from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
)

# ----------------------------
# Customer Details
# ----------------------------
CUSTOMER_NUMBER = "+919867005139"

# ----------------------------
# IMPORTANT
# Replace with your Render URL after deployment
# Example:
# https://vercel-jdd66ecnx-nikhilpatil100253-sudos-projects.vercel.app/voice
# ----------------------------
VOICE_URL = "https://vercel-jdd66ecnx-nikhilpatil100253-sudos-projects.vercel.app/voice"
# VOICE_URL = "insurance-voice-bot-n6hf-b0kgyspsy.vercel.app"

client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)

call = client.calls.create(
    to=CUSTOMER_NUMBER,
    from_=TWILIO_PHONE_NUMBER,
    url="https://vercel-jdd66ecnx-nikhilpatil100253-sudos-projects.vercel.app/voice",
    status_callback="https://vercel-jdd66ecnx-nikhilpatil100253-sudos-projects.vercel.app/status",
    status_callback_event=[
        "initiated",
        "ringing",
        "answered",
        "completed"
    ],
    status_callback_method="POST"
)

print("=" * 50)
print("Call Initiated Successfully")
print("Call SID :", call.sid)
print("=" * 50)