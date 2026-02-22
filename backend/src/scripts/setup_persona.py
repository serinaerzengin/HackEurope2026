"""
One-time script to create a Tavus interviewer persona.

Usage:
    cd backend
    python -m scripts.setup_persona

After running, copy the printed persona_id into your .env as TAVUS_PERSONA_ID.
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")
TAVUS_REPLICA_ID = os.getenv("TAVUS_REPLICA_ID", "r5dc7c7d0bcb")

SYSTEM_PROMPT = """\
You are a senior software engineer conducting a technical interview. \
You are friendly, professional, and encouraging. \
You ask clarifying questions, give hints when the candidate is stuck, \
and evaluate their problem-solving approach. \
The specific interview task will be provided in the conversational context — \
always refer to that task during the interview. \
Keep your responses concise and conversational.\
"""


def main():
    if not TAVUS_API_KEY:
        print("Error: TAVUS_API_KEY not set in .env")
        return

    resp = httpx.post(
        "https://tavusapi.com/v2/personas",
        headers={
            "x-api-key": TAVUS_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "persona_name": "Tech Interviewer",
            "system_prompt": SYSTEM_PROMPT,
            "default_replica_id": TAVUS_REPLICA_ID,
            "pipeline_mode": "full",
            "layers": {
                "perception": {
                    "perception_model": "raven-1",
                },
                "conversational_flow": {
                    "turn_detection_model": "sparrow-1",
                    "turn_taking_patience": "low",
                },
            },
        },
        timeout=30.0,
    )
    if not resp.is_success:
        print(f"Error {resp.status_code}: {resp.text}")
        return
    data = resp.json()
    persona_id = data.get("persona_id")
    print(f"Persona created successfully!")
    print(f"persona_id: {persona_id}")
    print(f"\nAdd this to your .env file:")
    print(f"TAVUS_PERSONA_ID={persona_id}")


if __name__ == "__main__":
    main()
