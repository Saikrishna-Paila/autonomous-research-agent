"""
Research Agent Node
==================

YOUR TASK: Implement the agent node that calls Claude with tools

This is the "brain" of the agent. It:
1. Receives the current state
2. Calls Claude with the tools
3. Returns the updated state with Claude's response

KEY CONCEPTS:
- The agent node is called repeatedly in a loop
- Claude decides which tool to call (or to finish)
- Tool results are automatically added to messages

HINTS:
- Use ChatAnthropic from langchain_anthropic
- Bind tools using model.bind_tools(tools)
- Access state["messages"] for conversation history

IMPORTS YOU'LL NEED:
-------------------
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from .state import AgentState
from .prompts import RESEARCH_AGENT_PROMPT

EXAMPLE STRUCTURE:
-----------------
def create_agent(tools: list):
    '''
    Create the Claude agent with tools bound.

    Args:
        tools: List of tools the agent can use

    Returns:
        Agent model with tools bound
    '''
    # YOUR CODE HERE
    # 1. Create ChatAnthropic model
    # 2. Bind tools to the model
    # 3. Return the model
    pass


def agent_node(state: AgentState) -> dict:
    '''
    The agent node - calls Claude and returns response.

    This function is called by LangGraph in each iteration.

    Args:
        state: Current agent state

    Returns:
        dict with "messages" key containing Claude's response
    '''
    # YOUR CODE HERE
    # 1. Get messages from state
    # 2. Add system message if first iteration
    # 3. Call the model
    # 4. Return {"messages": [response]}
    pass

"""

# ============================================
# YOUR CODE BELOW
# ============================================

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from .state import AgentState
from .prompts import RESEARCH_AGENT_PROMPT
from .tools.search import search_web

tools = [search_web]


def create_agent():
    """
    Create Claude agent with tools bound.
    """
    model = ChatAnthropic(
        api_key=ANTHROPIC_API_KEY,
        model=CLAUDE_MODEL,
        temperature=0
    )
    model_with_tools = model.bind_tools(tools)
    return model_with_tools


# Create the agent instance
agent = create_agent()


def agent_node(state: AgentState) -> dict:
    """
    The agent node - calls Claude and returns response.
    """
    messages = list(state["messages"])
    query = state["query"]

    # ALWAYS include system message at the start
    system_msg = SystemMessage(content=RESEARCH_AGENT_PROMPT)

    if not messages:
        # First iteration: add system message and user query
        messages = [
            system_msg,
            HumanMessage(content=f"Research this topic thoroughly and provide a comprehensive report: {query}")
        ]
    else:
        # Subsequent iterations: ensure system message is first
        # Filter out any existing system messages and add fresh one
        non_system_msgs = [m for m in messages if not isinstance(m, SystemMessage)]
        messages = [system_msg] + non_system_msgs

    response = agent.invoke(messages)

    return {"messages": [response]}



