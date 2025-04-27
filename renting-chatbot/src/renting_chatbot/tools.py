from loguru import logger
from pydantic import Field
from typing import Dict, Any
# from dotenv import load_dotenv

# from langgraph.errors import NodeInterrupt
from langchain.tools.base import StructuredTool


def schedule_a_meeting(
    preferred_date: str = Field(..., description="The date of the meeting"),
    preferred_time: str = Field(..., description="The time of the meeting"),
    lead_name: str = Field(..., description="The name of the lead"),
    address: str = Field(..., description="The address of the lead"),
) -> Dict[str, Any]:
    """Schedule a meeting with the lead"""
    logger.info(f"===> Scheduling a meeting for {lead_name} at {preferred_date} at {preferred_time}, address: {address}")
    return {"status": "confirmed"}


def trigger_communication(
    lead_name: str = Field(..., description="The name of the lead"),
    datetime: str = Field(..., description="The datetime of the event"),
    address: str = Field(..., description="The address of the lead"),
) -> Dict[str, Any]:
    """Trigger communication with the internal staff"""
    logger.info(f"===> Triggering communication for {lead_name} at {datetime} at {address}")
    return {"status": "triggered"}

# Define the tools that the agent can use
ScheduleMeetingTool = StructuredTool.from_function(schedule_a_meeting)
TriggerCommunicationTool = StructuredTool.from_function(trigger_communication)

homeowner_tools = [ScheduleMeetingTool, TriggerCommunicationTool]
renter_tools = []
