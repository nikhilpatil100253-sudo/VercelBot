from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai_service import get_ai_response, SYSTEM_PROMPT
from transcript import save_transcript
from supabase_service import (
    create_call,
    update_call,
    update_status,
    get_calls
)
from analysis_service import analyze_call
from whatsapp_service import send_whatsapp
import json
import time
app = Flask(__name__)

# Store conversations per call
conversation_memory = {}


@app.route("/")
def home():
    return "Insurance AI Voice Bot Running Successfully"


@app.route("/voice", methods=["POST"])
def voice():

    call_sid = request.form.get("CallSid")
    create_call(
        call_sid=call_sid,
        customer_name="Nikhil Patil",
        phone_number="+919867005139",
        policy_number="Tata123"
    )
    conversation_memory[call_sid] = {
        "history": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ],
        "send_whatsapp": False,
        "document": "",
        "customer_phone": "+919867005139"
    }

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="https://vercel-jdd66ecnx-nikhilpatil100253-sudos-projects.vercel.app/process",
        method="POST",
        speech_timeout="auto",
        language="en-IN"
    )

    gather.say(
        """
        Hello Nikhil.

        Welcome to Tata Insurance.

        I am your AI Assistant.

        Can you please confirm your policy number?
        """,
        language="en-IN"
    )

    response.append(gather)

    return str(response)



@app.route("/process", methods=["POST"])
def process():

    call_sid = request.form.get("CallSid")

    speech = request.form.get("SpeechResult", "")

    print("Customer :", speech)

    save_transcript("Customer", speech)

    memory = conversation_memory.get(call_sid)

    history = memory["history"]

    history.append(
        {
            "role": "user",
            "content": speech
        }
    )
    # Keep only recent conversation to reduce latency
    if len(history) > 7:
        history = [history[0]] + history[-6:]

    memory["history"] = history
    ai_response = get_ai_response(history)
    try:
        result = json.loads(ai_response)

        reply = result["reply"]

        should_send_whatsapp = result["send_whatsapp"]

        document = result["document"]
        if should_send_whatsapp:
            memory["send_whatsapp"] = True
            memory["document"] = document
    except Exception:
        reply = ai_response
        should_send_whatsapp = False
        document = ""

    print("Bot :", reply)

    save_transcript("Bot", reply)

    history.append(
        {
            "role": "assistant",
            "content": reply
        })

    conversation_memory[call_sid] = memory

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="https://vercel-jdd66ecnx-nikhilpatil100253-sudos-projects.vercel.app/process",
        method="POST",
        speech_timeout="auto",
        language="en-IN"
    )
    gather.say(
        reply,
        language="en-IN"
    )

    response.append(gather)

    return str(response)

@app.route("/status", methods=["POST"])
def status():

    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")

    print("Call SID:", call_sid)
    print("Call Status:", call_status)

    if call_status.lower() == "completed":

        memory = conversation_memory.get(call_sid)

        if not memory:
            return "OK"

        history = memory["history"]

        full_transcript = ""

        for msg in history:
            if msg["role"] != "system":
                full_transcript += f"{msg['role']}: {msg['content']}\n"

        analysis = analyze_call(full_transcript)
        # memory = conversation_memory.get(call_sid)

        if memory and memory["send_whatsapp"]:

            message = f"""Hi Nikhil 👋

            Thank you for speaking with Tata Insurance.

            As requested during our call, here is a recommended insurance plan.

            🏥 Tata Health Secure Plus

            ✅ Sum Insured: ₹10,00,000
            ✅ Annual Premium: ₹18,500
            ✅ Cashless Hospitals: 7,000+
            ✅ No Claim Bonus: Up to 100%
            ✅ Pre & Post Hospitalization Cover
            ✅ Family Floater Available

            If you'd like to know more or purchase this plan, simply reply to this WhatsApp message or contact our advisor.

            Thank you,
            Tata Insurance
            """

            print("========== WhatsApp Debug ==========")
            print("Customer Phone:", memory["customer_phone"])
            print("Send WhatsApp Flag:", memory["send_whatsapp"])
            print("Document:", memory["document"])
            print("===================================")

            try:
                sid = send_whatsapp(
                    memory["customer_phone"],
                    message
                )

                print("✅ WhatsApp Sent Successfully")
                print("Message SID:", sid)

            except Exception as e:
                print("❌ WhatsApp Error:", str(e))

        update_call(
            call_sid=call_sid,
            status="Completed",
            transcript=full_transcript,
            summary=analysis["summary"],
            sentiment=analysis["sentiment"],
            customer_interest=analysis["customer_interest"],
            call_outcome=analysis["call_outcome"],
            follow_up_required=analysis["follow_up_required"],
            follow_up_reason=analysis["follow_up_reason"],
            ai_summary=analysis["summary"]
        )

        conversation_memory.pop(call_sid, None)

    else:
        update_status(call_sid, call_status)

    return "OK"
@app.route("/calls")
def calls():
    return get_calls()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )




