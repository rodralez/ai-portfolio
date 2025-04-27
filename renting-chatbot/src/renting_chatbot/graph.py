from dotenv import load_dotenv
from loguru import logger
from typing import Literal

from langgraph.graph import StateGraph
from langgraph.graph import START, StateGraph # END
from langgraph.checkpoint.memory import MemorySaver

from src.renting_chatbot.configuration import Configuration
from src.renting_chatbot.state import State, OutputState
from src.renting_chatbot.agents import welcome_node, homeowner_node, resident_node

# We need this because we want to enable threads (conversations)
checkpointer = MemorySaver()

# Load environment variables from the .env file (if it exists)
status = load_dotenv()

if status:
    logger.info("Environment variables loaded successfully.")
else:
    logger.info("No environment variables found.")


def welcome_routing_node(state: State) -> Literal["homeowner", "resident", "welcome"]:
    if state.welcome_complete:
        if state.client_type == "homeowner":
            return "homeowner"
        elif state.client_type == "resident":
            return "resident"
        else:
            return "welcome"
    else:
        return "welcome"


def homeowner_routing_node(state: State) -> Literal["homeowner", "__end__" ]:
    if state.homeowner_is_onboarded:
        return "__end__"
    else:
        return "homeowner"


def resident_routing_node(state: State) -> Literal["resident", "__end__" ]:
    if state.resident_is_onboarded:
        return "__end__"
    else:
        return "resident"

# Create the graph
workflow = StateGraph(
    State, output=OutputState, config_schema=Configuration
)

# Add nodes
workflow.add_node("welcome", welcome_node)
workflow.add_node("homeowner", homeowner_node)
workflow.add_node("resident", resident_node)

# Define the edges and control flow
workflow.add_edge(START, "welcome")
workflow.add_conditional_edges("welcome", welcome_routing_node)
workflow.add_conditional_edges("homeowner", homeowner_routing_node)
workflow.add_conditional_edges("resident", resident_routing_node)

# Compile the graph
graph = workflow.compile(
    # checkpointer=checkpointer, # Comment to run LangGraph Studio
    interrupt_after=["welcome", "homeowner", "resident"],
)

graph.name = "RentingChatbot"
