import pprint
import functools
import operator
from typing import Type, Optional, List

from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor

from ..utls import log, ModelFactory 
from ..agnts import (
    create_agent_executor,
    should_invoke_tools,
    invoke_tools,
    AgentState,
)


def build_agnt_with_tools_graph(
        sys_prompt: str, 
        tools: List[Tool], 
        state_type: Optional[Type] = AgentState, 
        agnt_name: Optional[str] = "agent"
):

    tool_executor = ToolExecutor(tools)

    prompt = ChatPromptTemplate.from_messages(
        [("system", sys_prompt), MessagesPlaceholder(variable_name="messages")]
    )

    model = ModelFactory.create().bind_tools(tools)
    chain = prompt | model
    agent_node = create_agent_executor(chain=chain)

    graph = StateGraph(state_type)

    graph.add_node(agnt_name, agent_node)
    graph.add_node(
        "invoke_tools", functools.partial(invoke_tools, tool_executor=tool_executor)
    )

    graph.add_edge(START, agnt_name)

    graph.add_conditional_edges(
        agnt_name,
        should_invoke_tools,
        {
            "invoke_tools": "invoke_tools",
            "continue": END,
        },
    )

    graph.add_edge("invoke_tools", agnt_name)
    graph.add_edge(agnt_name, END)

    return graph.compile()
