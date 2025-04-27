import json
from pathlib import Path
from typing import Optional, Any
# from loguru import logger

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.errors import NodeInterrupt

from src.renting_chatbot.configuration import Configuration

# # Get the parent directory of the script
# parent_dir = Path(__file__).resolve().parent.parent.parent

# # Add the parent directory to sys.path
# sys.path.append(str(parent_dir))

# # Get the parent directory of the script
# parent_dir = Path(__file__).resolve().parent.parent


def init_model(config: Optional[RunnableConfig] = None) -> BaseChatModel:
    """Initialize the configured chat model."""
    configuration = Configuration.from_runnable_config(config)
    fully_specified_name = configuration.model
    if "/" in fully_specified_name:
        provider, model = fully_specified_name.split("/", maxsplit=1)
    else:
        provider = None
        model = fully_specified_name
    return init_chat_model(model, model_provider=provider)


def extract_json_from_message(message: str) -> dict:
    """Extract a JSON object from a message."""
    if "{" in message and "}" in message:
        json_start = message.find("{")
        json_end = message.rfind("}") + 1
        json_str = message[json_start:json_end]
        return json.loads(json_str)
    else:
        return None