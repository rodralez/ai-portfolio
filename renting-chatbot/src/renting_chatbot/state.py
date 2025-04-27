from dataclasses import dataclass, field
from pydantic import BaseModel
from typing_extensions import Annotated, TypedDict
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, ToolMessage
from langgraph.managed import IsLastStep, RemainingSteps
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage
StructuredResponse = Union[dict, BaseModel]

class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    is_last_step: IsLastStep
    remaining_steps: RemainingSteps
    structured_response: StructuredResponse

# GRAPH STATES
# @dataclass(kw_only=True)
# class InputState:
#     """Input state defines the interface between the graph and the user (external API)."""
#     messages: Annotated[List[AnyMessage], add_messages]
#     welcome_complete: bool = False
#     client_type: Literal["homeowner", "resident", "unsure"] = "unsure"

@dataclass(kw_only=True)
class State:
    """The state of the graph."""
    response: str = ""
    messages: Annotated[List[AnyMessage], add_messages]
    # Welcome agent
    welcome_complete: bool = False
    client_type: Literal["homeowner", "resident", "unsure"] = "unsure"
    # Homeowner agent
    homeowner_name: str = ""
    homeowner_contact: str = ""
    homeowner_home_address: str = ""
    homeowner_meeting_datetime: str = ""
    homeowner_is_vacant: bool = False
    homeowner_are_utilities_on: bool = False
    homeowner_is_onboarded: bool = False
    # Resident agent
    resident_is_onboarded: bool = False

# @dataclass(kw_only=True)
class OutputState():
    """The response object for the end user.
    This class defines the structure of the output that will be provided
    to the user after the graph's execution is complete.
    """
    response: str = ""
    messages: Annotated[List[AnyMessage], add_messages]
    pass
