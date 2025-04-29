from dataclasses import dataclass #, field
from typing_extensions import Annotated #, TypedDict
from typing import (
    Literal,
    List,
    # Any,
    # Callable,
    # Optional,
    # Sequence,
    # Type,
    # TypeVar,
    # Union,
    # cast,
)

from langchain_core.messages import AnyMessage # BaseMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.graph import add_messages

# @dataclass(kw_only=True)
# class InputState:
#     """Input state defines the interface between the graph and the user (external API)."""
#     messages: Annotated[List[AnyMessage], add_messages]
#     welcome_complete: bool = False
#     client_type: Literal["homeowner", "resident", "unsure"] = "unsure"

@dataclass(kw_only=True)
class State:
    """The state of the graph."""
    messages: Annotated[List[AnyMessage], add_messages]
    # Welcome agent
    client_type: Literal["homeowner", "resident", "unsure"] = "unsure"
    welcome_complete: bool = False
    # Homeowner agent
    homeowner_is_onboarded: bool = False
    # Resident agent
    resident_is_onboarded: bool = False
    next_node: Literal["welcome", "homeowner", "resident", "user"] = "welcome"
  
# @dataclass(kw_only=True)
class OutputState():
    """The response object for the end user.
    This class defines the structure of the output that will be provided
    to the user after the graph's execution is complete.
    """
    messages: Annotated[List[AnyMessage], add_messages]
