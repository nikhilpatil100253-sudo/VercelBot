import json

from openai_service import (
    client,
    AZURE_OPENAI_DEPLOYMENT
)


def analyze_call(transcript):

    prompt = f"""
You are a Quality Assurance Manager for an insurance company.

Analyze the complete customer conversation.

Return ONLY valid JSON in the following format.

{{
    "summary": "",
    "sentiment": "Positive | Neutral | Negative",
    "customer_interest": "Interested | Not Interested | Callback Requested | Existing Customer | Wrong Number",
    "call_outcome": "Successful | Follow-up Required | Unsuccessful",
    "follow_up_required": true,
    "follow_up_reason": ""
}}

Conversation:

{transcript}
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return json.loads(
        response.choices[0].message.content
    )