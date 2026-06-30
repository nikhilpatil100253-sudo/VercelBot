from datetime import datetime

def save_transcript(role, message):
    with open("transcript.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {role}: {message}\n")