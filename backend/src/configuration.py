from dotenv import load_dotenv
import os

load_dotenv()

# Load API keys from environment variables
PAID_API_KEY = os.getenv("PAID_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_ORG_ID = os.getenv("LANGSMITH_ORG_ID")

TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")
TAVUS_PERSONA_ID = os.getenv("TAVUS_PERSONA_ID")
TAVUS_REPLICA_ID = os.getenv("TAVUS_REPLICA_ID", "r5dc7c7d0bcb")

MIRO_BOARD_ID = os.getenv("MIRO_BOARD_ID")
MIRO_ACCESS_TOKEN = os.getenv("MIRO_ACCESS_TOKEN")  # set this in your environment
