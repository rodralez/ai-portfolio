import os
import sys
import asyncio
from loguru import logger

# from langgraph.types import Command
from langgraph.errors import NodeInterrupt
from langchain_core.messages import HumanMessage #, ToolMessage, AIMessage, AnyMessage, SystemMessage, 

 # Get the parent directory of the script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from src.renting_chatbot import graph

async def test_graph() -> None:

    thread_config = {
        "configurable": {
            "thread_id": "1265458",
        },
        # "metadata": {
        # }        
    }

    messages = [
        # [HumanMessage(content= "Hello, how are you?")],
        # [HumanMessage(content= "Hello, I am a homeowner")]
        [HumanMessage(content= "Hello, I am a resident")],
        [HumanMessage(content= "I am looking for a place to live in Denver")],
    ]
 
    try:
        for message in messages:
            result = await graph.ainvoke({"messages": message}, config=thread_config)
            logger.info(result)
            # async for chunk in graph.astream({"messages": message}, config=thread_config, stream_mode="values"):
            #    logger.info(result)
    except NodeInterrupt as e:
        logger.info(e)
        return e
    except Exception as e:
        logger.error(e)

    # Get the graph state to get interrupt information
    state = graph.get_state(thread_config)

    messages = state.values['messages']
    for message in messages:
        logger.info(message.content)

    assert "messages" in result, "Expected response in result"
    print("All assertions passed!")


if __name__ == "__main__":
    asyncio.run(test_graph())
