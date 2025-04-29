import os
from loguru import logger
from datetime import datetime

from langgraph.prebuilt import create_react_agent
from langgraph.errors import NodeInterrupt
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage #AIMessage AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage, trim_messages
from langgraph.types import interrupt, Command

from src.renting_chatbot.state import State
from src.renting_chatbot.prompts import WELCOME_AGENT_PROMPT, HOMEOWNER_AGENT_PROMPT, RESIDENT_AGENT_PROMPT
from src.renting_chatbot.utils import init_model
from src.renting_chatbot.utils import extract_json_from_message
from src.renting_chatbot.tools import homeowner_tools, resident_tools


def welcome_node(state: State, config: dict):
    """Define the agent function that invokes the model"""
    logger.info("Welcome agent...")

    messages = state.messages
    if messages is None:
        raise NodeInterrupt("No messages provided to the welcome agent.")

    messages_length = len(messages)
    if messages_length <= 1:
        first_message = "Yes"
    else:
        first_message = "No"
    try:
        # replace placeholder with messages from state
        p = WELCOME_AGENT_PROMPT.format(
            messages = messages,
            company_name = os.getenv("COMPANY_NAME"),
            first_message = first_message
        )

        raw_model = init_model(config)
        welcome_agent = create_react_agent(
                                    model = raw_model, 
                                    tools = [], 
                                    prompt = p,
                                    # response_format=WelcomeAgentResponse,
                                    # state_schema=CustomAgentState,
                                    # debug=True,
                            )

        response = welcome_agent.invoke({"messages": messages}, config = config )

        last_message = response['messages'][-1].content
        # Check if the content is a valid JSON string
        result = extract_json_from_message(last_message)

        # Parse the JSON from the last message to extract onboarding_complete and client_type
        
        if result is not None:
            ai_response = result.get("message", "")

            client_type = result.get("client_type", "unsure")
            welcome_complete = result.get("welcome_complete", False)

            logger.info(f"Welcome agent, AI response: {ai_response}")
            logger.info(f"Welcome agent, client type: {client_type}")
            logger.info(f"Welcome agent, welcome complete: {welcome_complete}")

            return {
                "messages": response['messages'],
                "welcome_complete": welcome_complete,
                "client_type": client_type,
                "next_node": "welcome"
            }
        else:
            logger.error(f"Error parsing JSON from welcome agent: {last_message}")
    except Exception as e:
        logger.error(f"Error parsing JSON from welcome agent: {e}")
        raise NodeInterrupt("Error parsing JSON from welcome agent")


def homeowner_node(state: State, config: dict):
    """Define the agent function that invokes the model"""
    logger.info("Homeowner agent...")

    messages = state.messages
    if messages is None:
        raise NodeInterrupt("No messages provided to the agent.")
    try:
        p = HOMEOWNER_AGENT_PROMPT.format(
            messages = messages,
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        raw_model = init_model(config)
        homeowner_agent = create_react_agent(
                                    model = raw_model, 
                                    tools = homeowner_tools,
                                    prompt = p,
                                    )

        response = homeowner_agent.invoke({"messages": messages}, config = config )

        last_message = response['messages'][-1].content
        # Check if the content is a valid JSON string
        result = extract_json_from_message(last_message)

        if result is not None:
            ai_response = result.get("message", "")
            homeowner_name = result.get("name", None)
            homeowner_contact = result.get("contact", None)
            homeowner_home_address = result.get("address", None)
            homeowner_meeting_datetime = result.get("meeting_datetime", None)
            is_home_vacant = result.get("is_vacant", False)
            are_home_utilities_on = result.get("utilities_on", False)
            onboarding_complete = result.get("onboarding_complete", False)

            logger.info(f"Homeowner agent, AI response: {ai_response}")
            logger.info(f"Homeowner agent, name: {homeowner_name}")
            logger.info(f"Homeowner agent, contact: {homeowner_contact}")
            logger.info(f"Homeowner agent, home address: {homeowner_home_address}")
            logger.info(f"Homeowner agent, meeting datetime: {homeowner_meeting_datetime}")
            logger.info(f"Homeowner agent, is vacant: {is_home_vacant}")
            logger.info(f"Homeowner agent, are utilities on: {are_home_utilities_on}")
            logger.info(f"Homeowner agent, homeowner is onboarded: {onboarding_complete}")

            return {
                "messages": response['messages'],
                "homeowner_is_onboarded": onboarding_complete,
                "next_node": "homeowner"
            }
        else:
            logger.error(f"Error parsing JSON from homeowner agent: {last_message}")
    except Exception as e:
        logger.error(f"Error parsing JSON from homeowner agent: {e}")
        raise NodeInterrupt("Error parsing JSON from homeowner agent")


def resident_node(state: State, config: dict):
    """Define the agent function that invokes the model"""
    logger.info("Resident agent...")

    messages = state.messages
    if messages is None:
        raise NodeInterrupt("No messages provided to the agent.")
    try:
        p = RESIDENT_AGENT_PROMPT.format(
            messages = messages,
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        raw_model = init_model(config)
        resident_agent = create_react_agent(
                                    model = raw_model, 
                                    tools = resident_tools, 
                                    prompt = p,
                                    )
        response = resident_agent.invoke({"messages": messages}, config = config )

        last_message = response['messages'][-1].content
        # Check if the content is a valid JSON string
        result = extract_json_from_message(last_message)

        if result is not None:
            ai_response = result.get("message", "")
            resident_name = result.get("name", "")
            resident_contact = result.get("contact", "")
            bedrooms = result.get("bedrooms", 0)
            bathrooms = result.get("bathrooms", 0)
            city = result.get("city", "")
            budget = result.get("budget", 0.0)
            additional_preferences = result.get("additional_preferences", "")
            selected_listing_id = result.get("selected_listing_id", "")
            tour_datetime = result.get("tour_datetime", "")
            onboarding_complete = result.get("onboarding_complete", False)

            logger.info(f"Resident agent, AI response: {ai_response}")
            logger.info(f"Resident agent, ai response: {ai_response}")
            logger.info(f"Resident agent, name: {resident_name}")
            logger.info(f"Resident agent, contact: {resident_contact}")
            logger.info(f"Resident agent, bedrooms: {bedrooms}")
            logger.info(f"Resident agent, bathrooms: {bathrooms}")
            logger.info(f"Resident agent, city: {city}")
            logger.info(f"Resident agent, budget: {budget}")
            logger.info(f"Resident agent, additional preferences: {additional_preferences}")
            logger.info(f"Resident agent, selected listing id: {selected_listing_id}")
            logger.info(f"Resident agent, tour datetime: {tour_datetime}")
            logger.info(f"Resident agent, onboarding complete: {onboarding_complete}")

            return {
                "messages": response['messages'],
                "resident_is_onboarded": onboarding_complete,
                "next_node": "resident"
            }
        else:
            logger.error(f"Error parsing JSON from resident agent: {last_message}")
    except Exception as e:
        logger.error(f"Error parsing JSON from resident agent: {e}")
        raise NodeInterrupt("Error parsing JSON from resident agent")


from typing import Literal

def user_node(state: State) -> Command[Literal['welcome', 'homeowner', 'resident']]:
    """A node for collecting user input."""
    logger.info("User node...")

    last_message = state.messages[-1].content
    result = extract_json_from_message(last_message)

    if result is not None:
        ai_query = result.get("message", "")
    else:
        ai_query = state.messages[-1].content

    logger.info(f"User node, query: {ai_query}")
    logger.info(f"User node, next node: {state.next_node}")

    user_input = interrupt(value=ai_query)
    logger.info(f"User node, user input: {user_input}")

    return {
           "messages": [HumanMessage(content=user_input)],
           "next_node": state.next_node
           }
