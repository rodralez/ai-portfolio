from loguru import logger
from pydantic import Field
from typing import Dict, Any

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
    event: str = Field(..., description="The event to trigger"),
    datetime: str = Field(..., description="The datetime of the event"),
    address: str = Field(..., description="The address of the lead"),
    contact: str = Field(..., description="Phone or email contact information"),
    listing_id: str = Field(None, description="The ID of the listing") 
) -> Dict[str, Any]:
    """Trigger communication with the internal staff"""
    logger.info(f"===> Triggering communication for event {event}")
    logger.info(f"     Lead Name: {lead_name}")
    logger.info(f"     Date/Time: {datetime}")
    logger.info(f"     Contact: {contact}")
    logger.info(f"     Address: {address}")
    if listing_id:
        logger.info(f"     Listing ID: {listing_id}")

    return {"status": "triggered"}


def fetch_listings(
    bedrooms: int = Field(..., description="Number of bedrooms desired"),
    bathrooms: int = Field(..., description="Number of bathrooms desired"), 
    city: str = Field(..., description="Desired city/area"),
    budget: float = Field(None, description="Monthly budget (optional)"),
    preferences: str = Field(None, description="Additional preferences (optional)")
) -> Dict[str, Any]:
    """Fetch available listings matching the criteria"""
    logger.info(f"===> Fetching listings: {bedrooms} bed, {bathrooms} bath in {city}")
    logger.info(f"     Budget: {budget}, Preferences: {preferences}")
    
    # Mock response with sample listings
    return {
        "listings": [
            {"id": "H123", "address": "45 Oak St", "price": 1200},
            {"id": "H124", "address": "78 Pine Ave", "price": 1250}, 
            {"id": "H125", "address": "22 Cedar Ln", "price": 1300}
        ]
    }

def schedule_tour(
    listing_id: str = Field(..., description="ID of the listing"),
    preferred_date: str = Field(..., description="The preferred date for the tour (YYYY-MM-DD)"),
    preferred_time: str = Field(..., description="The preferred time for the tour (HH:MM)"),
    resident_name: str = Field(..., description="The name of the renter"),
    contact: str = Field(..., description="Phone or email contact information")
) -> Dict[str, Any]:
    """Schedule a tour for a specific listing"""
    logger.info(f"===> Scheduling tour for listing {listing_id}")
    logger.info(f"     Resident: {resident_name}, Contact: {contact}")
    logger.info(f"     Date/Time: {preferred_date} at {preferred_time}")

    return {"status": "confirmed"}

# Define the tools that the agent can use
ScheduleMeetingTool = StructuredTool.from_function(schedule_a_meeting)
ScheduleTourTool = StructuredTool.from_function(schedule_tour)
TriggerCommunicationTool = StructuredTool.from_function(trigger_communication)
FetchListingsTool = StructuredTool.from_function(fetch_listings)

homeowner_tools = [ScheduleMeetingTool, TriggerCommunicationTool]
resident_tools = [FetchListingsTool, ScheduleTourTool, TriggerCommunicationTool]
