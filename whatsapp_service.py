import os
from twilio.rest import Client

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

FROM_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")


def send_whatsapp(phone, message):

    msg = client.messages.create(

        from_=FROM_NUMBER,

        to=f"whatsapp:{phone}",

        body=message

    )

    print("WhatsApp SID:", msg.sid)

    return msg.sid