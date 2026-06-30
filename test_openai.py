from openai_service import get_ai_response, SYSTEM_PROMPT

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Hello"},
]

response = get_ai_response(messages)

print(response)
