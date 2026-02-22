"""
Diagram Analysis Agent — uses the OFFICIAL Miro MCP server (https://mcp.miro.com/)
via langchain-mcp-adapters to fetch and analyze system design diagrams.

Tools available from Miro MCP: context_explore, board_list_items, context_get, etc.
Auth: OAuth 2.1 with PKCE (browser flow on first use, tokens cached on disk).
"""

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from src.configuration import MIRO_BOARD_ID


class DiagramAnalysis(BaseModel):
    summary: str = Field(description="2-3 sentence overview of the architecture")
    components: list[str] = Field(description="Identified system components with their roles")
    connections: list[str] = Field(description="Data flows and relationships between components")
    potential_issues: list[str] = Field(description="Gaps, missing elements, or architectural concerns")
    probe_areas: list[str] = Field(description="Specific questions to ask the candidate about their design")


DIAGRAM_SYSTEM_PROMPT = """You are a senior system design interviewer analyzing a candidate's architecture diagram on a Miro board.

The board ID is: {board_id}
The board URL is: https://miro.com/app/board/{board_id}/

IMPORTANT: When calling Miro tools, always use the FULL board URL: https://miro.com/app/board/{board_id}/

You have access to Miro MCP tools. Use them in this order:

1. First, call context_explore with the board URL to discover what's on the board (frames, items, structure)
2. Call board_list_items with the board URL to get all shapes, sticky notes, text, connectors
3. For any interesting frames or items, call context_get with the specific item URL to get detailed content

From the board contents, analyze:

1. **Components**: Every system component (services, databases, caches, queues, load balancers, APIs, clients).
   Use the text labels on shapes. If a shape has no text, infer from shape type and position.

2. **Connections**: Data flows between components. Look for connectors/arrows and their labels.
   Also infer relationships from item proximity if explicit connectors are missing.

3. **Potential Issues**:
   - Missing components (no database? no cache? no auth? no monitoring?)
   - Single points of failure
   - Scalability concerns
   - Missing data flows between components that should be connected

4. **Probe Areas**: Specific interview questions referencing actual component names:
   - "How does X handle failures when calling Y?"
   - "What happens when Z goes down?"
   - "How would you scale this part if traffic increased 10x?"

Be concrete. Reference actual labels and text from the board.
If the board has very few items, note what's incomplete.
"""


async def analyze_diagram() -> DiagramAnalysis:
    """
    Connect to the official Miro MCP server, fetch board contents,
    and analyze the system design diagram using a ReAct agent.
    """
    from src.services.miro_mcp_auth import get_miro_mcp_access_token

    # Get OAuth token (cached or via browser flow)
    access_token = await get_miro_mcp_access_token()
    print(f"[diagram_agent] Got Miro MCP access token (len={len(access_token)})")

    model = init_chat_model("gpt-4.1", temperature=0)

    mcp_server_config = {
        "miro": {
            "transport": "http",
            "url": "https://mcp.miro.com/",
            "headers": {
                "Authorization": f"Bearer {access_token}",
            },
        }
    }

    client = MultiServerMCPClient(mcp_server_config)
    tools = await client.get_tools()
    tool_names = [t.name for t in tools]
    print(f"[diagram_agent] Miro MCP tools available ({len(tools)}): {tool_names}")

    if not tools:
        raise RuntimeError("No tools returned from Miro MCP server")

    agent = create_react_agent(
        model=model,
        tools=tools,
    )

    system_prompt = DIAGRAM_SYSTEM_PROMPT.format(board_id=MIRO_BOARD_ID)

    result = await agent.ainvoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Fetch and analyze the system design diagram on the Miro board. "
                    "Use the Miro tools to explore the board, list all items, and get context. "
                    "Then provide a comprehensive analysis of the architecture."
                ),
            },
        ]
    })

    # Extract the last AI message content
    last_message = result["messages"][-1]
    content = last_message.content if hasattr(last_message, "content") else str(last_message)
    print(f"[diagram_agent] Agent analysis complete ({len(content)} chars)")

    # Parse into structured format
    structured_model = model.with_structured_output(DiagramAnalysis)
    analysis = await structured_model.ainvoke([
        {"role": "system", "content": "Extract the diagram analysis into the structured format. Be specific and reference actual component names."},
        {"role": "user", "content": content},
    ])

    print(f"[diagram_agent] Structured analysis:")
    print(f"  Summary: {analysis.summary}")
    print(f"  Components: {len(analysis.components)}")
    print(f"  Connections: {len(analysis.connections)}")
    print(f"  Issues: {len(analysis.potential_issues)}")
    print(f"  Probe areas: {len(analysis.probe_areas)}")

    return analysis
