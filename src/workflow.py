"""
LangGraph Workflow Definition
============================

YOUR TASK: Build the LangGraph workflow that orchestrates the agent

This file defines:
1. The graph structure (nodes and edges)
2. The routing logic (when to use tools vs finish)
3. The compiled workflow

KEY CONCEPTS:
- StateGraph: The main graph class
- Nodes: Functions that process state
- Edges: Connections between nodes
- Conditional edges: Route based on logic

THE REACT PATTERN:
-----------------
    ┌─────────┐
    │  START  │
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  AGENT  │◄────────┐
    └────┬────┘         │
         │              │
         ▼              │
    ┌─────────┐         │
    │ ROUTER  │         │
    └────┬────┘         │
         │              │
    ┌────┴────┐         │
    │         │         │
    ▼         ▼         │
  TOOLS      END        │
    │                   │
    └───────────────────┘

IMPORTS YOU'LL NEED:
-------------------
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from .state import AgentState
from .agent import agent_node, create_agent
from .tools.search import search_web  # Your tool

EXAMPLE STRUCTURE:
-----------------
def should_continue(state: AgentState) -> str:
    '''
    Router function - decides next step.

    Returns:
        "tools" if agent wants to use a tool
        "end" if agent is done
    '''
    # YOUR CODE HERE
    # 1. Get the last message
    # 2. Check if it has tool_calls
    # 3. Return "tools" or "end"
    pass


def create_research_workflow():
    '''
    Create and compile the research agent workflow.

    Returns:
        Compiled LangGraph workflow
    '''
    # YOUR CODE HERE
    #
    # 1. Create the graph
    #    workflow = StateGraph(AgentState)
    #
    # 2. Add nodes
    #    workflow.add_node("agent", agent_node)
    #    workflow.add_node("tools", tool_node)
    #
    # 3. Set entry point
    #    workflow.set_entry_point("agent")
    #
    # 4. Add conditional edges
    #    workflow.add_conditional_edges(
    #        "agent",
    #        should_continue,
    #        {"tools": "tools", "end": END}
    #    )
    #
    # 5. Add edge from tools back to agent
    #    workflow.add_edge("tools", "agent")
    #
    # 6. Compile and return
    #    return workflow.compile()
    pass


# Create the workflow instance (will be imported by app)
# research_agent = create_research_workflow()

"""

# ============================================
# YOUR CODE BELOW
# ============================================

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from .state import AgentState
from .agent import agent_node, tools


def should_continue(state: AgentState) -> str:
    """
    Router function - decides next step.
    """
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return "end"


def create_research_workflow():
    """
    Create and compile the research agent workflow.
    """
    workflow = StateGraph(AgentState)

    tool_node = ToolNode(tools)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "end": END}
    )

    workflow.add_edge("tools", "agent")

    return workflow.compile()


# Create the workflow instance
research_agent = create_research_workflow()
