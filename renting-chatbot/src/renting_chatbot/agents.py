import os
from loguru import logger

from langgraph.prebuilt import create_react_agent
from langgraph.errors import NodeInterrupt
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage #AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage, trim_messages

from src.renting_chatbot.state import State
from src.renting_chatbot.prompts import WELCOME_AGENT_PROMPT, HOMEOWNER_AGENT_PROMPT, RENTER_AGENT_PROMPT
from src.renting_chatbot.utils import init_model
from src.renting_chatbot.utils import extract_json_from_message
from src.renting_chatbot.tools import homeowner_tools
# from src.renting_chatbot.configuration import Configuration
# from src.renting_chatbot.schemas import WelcomeAgentResponse


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
                                # checkpointer=checkpointer,
                        )

    response = welcome_agent.invoke({"messages": messages}, config = config )
    
    # Parse the JSON from the last message to extract onboarding_complete and client_type
    try:
        last_message = response['messages'][-1].content
        # Check if the content is a valid JSON string
        result = extract_json_from_message(last_message)
        
        if result is not None:
            message = result.get("message", "")
            client_type = result.get("client_type", "unsure")
            welcome_complete = result.get("welcome_complete", False)

            logger.info(f"Welcome agent, response: {message}")
            logger.info(f"Welcome agent, client type: {client_type}")
            logger.info(f"Welcome agent, welcome complete: {welcome_complete}")

            return {
                "messages": response['messages'],
                "welcome_complete": welcome_complete,
                "client_type": client_type,
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
    try:
        p = HOMEOWNER_AGENT_PROMPT.format(
            messages = messages,
        )

        raw_model = init_model(config)
        homeowner_agent = create_react_agent(
                                    model = raw_model, 
                                    tools = homeowner_tools,
                                    prompt = p,
                                    )
        # Parse the JSON from the last message to extract data
        response = homeowner_agent.invoke({"messages": messages}, config = config )
        
        last_message = response['messages'][-1].content
        # Check if the content is a valid JSON string
        result = extract_json_from_message(last_message)
        
        if result is not None:
            homeowner_name = result.get("name", None)
            homeowner_contact = result.get("contact", None)
            homeowner_home_address = result.get("address", None)
            homeowner_meeting_datetime = result.get("meeting_datetime", None)
            is_home_vacant = result.get("is_vacant", False)
            are_home_utilities_on = result.get("utilities_on", False)
            onboarding_complete = result.get("onboarding_complete", False)

            logger.info(f"Homeowner agent, name: {homeowner_name}")
            logger.info(f"Homeowner agent, contact: {homeowner_contact}")
            logger.info(f"Homeowner agent, home address: {homeowner_home_address}")
            logger.info(f"Homeowner agent, meeting datetime: {homeowner_meeting_datetime}")
            logger.info(f"Homeowner agent, is vacant: {is_home_vacant}")
            logger.info(f"Homeowner agent, are utilities on: {are_home_utilities_on}")
            logger.info(f"Homeowner agent, homeowner is onboarded: {onboarding_complete}")

            return {
                "messages": response['messages'],
                "homeowner_name": homeowner_name,
                "homeowner_contact": homeowner_contact,
                "homeowner_home_address": homeowner_home_address,
                "homeowner_meeting_datetime": homeowner_meeting_datetime,
                "homeowner_is_vacant": is_home_vacant,
                "homeowner_are_utilities_on": are_home_utilities_on,
                "homeowner_is_onboarded": onboarding_complete
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

    p = RENTER_AGENT_PROMPT.format(
        messages = messages,
        company_name = os.getenv("COMPANY_NAME")
    )
    
    raw_model = init_model(config)
    response = create_react_agent(
                                model = raw_model, 
                                tools = [], 
                                prompt = p,
                                )

    return {"messages": response['messages']}