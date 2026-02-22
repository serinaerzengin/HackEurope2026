import httpx
from src.configuration import TAVUS_API_KEY

TAVUS_API_BASE = "https://tavusapi.com/v2"


async def create_conversation(
    persona_id: str,
    replica_id: str,
    conversation_name: str,
    conversational_context: str,
    custom_greeting: str,
) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TAVUS_API_BASE}/conversations",
            headers={
                "x-api-key": TAVUS_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "persona_id": persona_id,
                "replica_id": replica_id,
                "conversation_name": conversation_name,
                "conversational_context": conversational_context,
                "custom_greeting": custom_greeting,
            },
            timeout=30.0,
        )
        if not resp.is_success:
            print(f"[tavus_client] Error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
        return resp.json()


async def end_conversation(conversation_id: str) -> None:
    """End a Tavus conversation. Swallows errors so callers don't crash."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.delete(
                f"{TAVUS_API_BASE}/conversations/{conversation_id}",
                headers={
                    "x-api-key": TAVUS_API_KEY,
                    "Content-Type": "application/json",
                },
                timeout=15.0,
            )
            if resp.is_success:
                print(f"[tavus_client] Ended conversation {conversation_id}")
            else:
                print(f"[tavus_client] End conversation {conversation_id} returned {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[tavus_client] Failed to end conversation {conversation_id}: {e}")
