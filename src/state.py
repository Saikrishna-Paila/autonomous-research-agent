"""
Agent State Definition
This defines the data structure that flows through the LangGraph agent
"""
from typing import TypedDict, List, Annotated
from langgraph.graph import add_messages


class ResearchFinding(TypedDict):
    """A single research finding from a search"""
    title: str
    content: str
    source: str
    query: str


class AgentState(TypedDict):
    """
    State that flows through the research agent.

    This is the "memory" of the agent - it contains everything
    the agent knows and has done.

    Attributes:
        query: The original research question from the user
        messages: Conversation history (LangGraph manages this)
        findings: List of research findings accumulated
        iteration: Current iteration count
        scratchpad: Agent's reasoning trace (for debugging)
        final_report: The generated report (when complete)
        is_complete: Whether the research is finished
    """

    # The original research query
    query: str

    # Message history - Annotated with add_messages for LangGraph
    # This automatically appends new messages instead of replacing
    messages: Annotated[list, add_messages]

    # Accumulated research findings
    findings: List[ResearchFinding]

    # Current iteration (to prevent infinite loops)
    iteration: int

    # Agent's reasoning trace
    scratchpad: str

    # Final output
    final_report: str

    # Completion flag
    is_complete: bool


def create_initial_state(query: str) -> AgentState:
    """
    Create the initial state for a new research query.

    Args:
        query: The research question to investigate

    Returns:
        AgentState: Initial state with empty findings
    """
    return {
        "query": query,
        "messages": [],
        "findings": [],
        "iteration": 0,
        "scratchpad": "",
        "final_report": "",
        "is_complete": False,
    }
