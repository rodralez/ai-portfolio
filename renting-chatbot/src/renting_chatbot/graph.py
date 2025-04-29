from loguru import logger
from typing import Literal
from dotenv import load_dotenv

from langgraph.graph import StateGraph
from langgraph.graph import START, StateGraph # END
from langgraph.checkpoint.memory import MemorySaver

from src.renting_chatbot.configuration import Configuration
from src.renting_chatbot.state import State, OutputState
from src.renting_chatbot.agents import welcome_node, homeowner_node, resident_node, user_node

# We need this because we want to enable threads (conversations)
checkpointer = MemorySaver()

# Load environment variables from the .env file (if it exists)
status = load_dotenv(dotenv_path='renting-chatbot/.env')
if status:
    logger.info("Environment variables loaded successfully.")
else:
    logger.info("No environment variables found.")
    
def welcome_routing_node(state: State) -> Literal["homeowner", "resident", "user"]:
    if state.welcome_complete:
        if state.client_type == "homeowner":
            node = "homeowner"
        elif state.client_type == "resident":
            node = "resident"
        else:
            node = "user"
    else:
        node = "user"    
    logger.info(f"Routing to {node} node")
    return node

def homeowner_routing_node(state: State) -> Literal["user", "__end__" ]:
    if state.homeowner_is_onboarded:
        node = "__end__"
    else:
        node = "user"
    logger.info(f"Routing to {node} node")
    return node


def resident_routing_node(state: State) -> Literal["user", "__end__" ]:
    if state.resident_is_onboarded:
        node = "__end__"
    else:
        node = "user"
    logger.info(f"Routing to {node} node")
    return node

def user_routing_node(state: State) -> Literal["welcome", "homeowner", "resident", "__end__" ]:
    if state.next_node == "welcome":
        node = "welcome"
    elif state.next_node == "homeowner":
        node = "homeowner"
    elif state.next_node == "resident":
        node = "resident"
    else:
        node = "__end__"
    logger.info(f"Routing to {node} node")
    return node
# Create the graph
workflow = StateGraph(
    State, output=OutputState, config_schema=Configuration
)

# Add nodes
workflow.add_node("welcome", welcome_node)
workflow.add_node("homeowner", homeowner_node)
workflow.add_node("resident", resident_node)
workflow.add_node("user", user_node)
# Define the edges and control flow

workflow.add_edge(START, "welcome")
workflow.add_conditional_edges("welcome", welcome_routing_node)
workflow.add_conditional_edges("homeowner", homeowner_routing_node)
workflow.add_conditional_edges("resident", resident_routing_node)
workflow.add_conditional_edges("user", user_routing_node)

# Compile the graph
graph = workflow.compile(
    # checkpointer=checkpointer, # Comment to run LangGraph Studio
    # interrupt_after=["welcome", "homeowner", "resident"],
)

graph.name = "RentingChatbot"
