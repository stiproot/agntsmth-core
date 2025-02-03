from typing import List, Any, Optional
import pprint
import logging
from langchain_core.runnables import Runnable
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation
from .agnt_state import GraphState
from ..utls import log


def create_agent_executor(
    chain: Runnable, messages_key: Optional[str] = "message_history"
):
    def invoke_chain(state: GraphState):
        log(f"{invoke_chain.__name__} START.")

        message_history = state[messages_key]

        output = chain.invoke({"message_history": message_history})

        message_history += [output]
        log(f"{invoke_chain.__name__} END.")

    return invoke_chain


def should_invoke_tools(state: GraphState):
    log(f"{should_invoke_tools.__name__} START.")

    message_history = state["message_history"]

    last_message = message_history[-1]

    if last_message.tool_calls:
        log(f"{should_invoke_tools.__name__} END. invoke_tools!")
        return "invoke_tools"

    log(f"{should_invoke_tools.__name__} END. continue!")
    return "continue"


def invoke_tools(state: GraphState, tool_executor):
    log(f"{invoke_tools.__name__} START.")

    message_history = state["message_history"]

    last_message = message_history[-1]
    tool_invocations = []

    for tool_call in last_message.tool_calls:
        action = ToolInvocation(
            tool=tool_call["name"],
            tool_input=tool_call["args"],
        )
        tool_invocations.append(action)

    responses = tool_executor.batch(tool_invocations, return_exceptions=True)

    tool_messages = [
        ToolMessage(
            content=str(response),
            name=tc["name"],
            tool_call_id=tc["id"],
        )
        for tc, response in zip(last_message.tool_calls, responses)
    ]

    log(f"{invoke_tools.__name__} END.")

    return {"message_history": tool_messages}
