from deepagents import create_deep_agent
from src.types.dto import TavusUtteranceResponse
from src.configuration import (
    OPENAI_API_KEY,
    FIRECRAWL_API_KEY,
    LANGSMITH_API_KEY,
    LANGSMITH_ORG_ID,
)


def run_agent(history: list[dict[str, str]]) -> TavusUtteranceResponse:
    """Run the interviewer agent with the given conversation history."""
    pass


def test_tool1():
    """test if the tool is working"""
    print("Testing the tool 1...")
    return 1


def test_tool2():
    """test if the tool is working"""
    print("Testing the tool 2...")
    return 2


# System prompt to steer the agent to be an expert researcher
instructions = """You are just a test agent, you have access to the subagent that wuill help you with your tastk. The subagent has access to the following tool:
## `test_tool`
# Use this tool to test if the agent can call it correctly. The tool will return 1 when called."""

subagent1 = {
    "name": "assistant",
    "description": "Assist the other agents in the system ",
    "system_prompt": """
        You are just a test agent, you have access to the following tool:

        ## `test_tool`

        Use this tool to test if the agent can call it correctly. The tool will return 1 when called.""",
    "tools": [test_tool1],
    "model": "openai:gpt-4.1",  # Optional override, defaults to main agent model
}

subagent2 = {
    "name": "assistant2",
    "description": "Assist the other agents in the system ",
    "system_prompt": """
        You are just a test agent, you have access to the following tool:

        ## `test_tool`

        Use this tool to test if the agent can call it correctly. The tool will return 1 when called.""",
    "tools": [test_tool2],
    "model": "openai:gpt-4.1",  # Optional override, defaults to main agent model
}

subagents = [subagent1, subagent2]
agent = create_deep_agent(
    model="gpt-4-0613",
    # tools=[test_tool],
    subagents=subagents,
    # system_prompt=instructions
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Please ask your subagents named 'assistant' and 'assistant2' to call the `test_tool1` and `test_tool2` respectively and return their results. Do NOT call the tools yourself; delegate them to the subagents.",
            }
        ]
    }
)

# Print the agent's response
print(result["messages"][-1].content)
