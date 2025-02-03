import pprint
import functools
import operator
from typing import Type, Optional, Callable

from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor

from ..utls import log, ModelFactory 
from ..agnts import (
    create_agent_executor,
    should_invoke_tools,
    invoke_tools,
    GraphState,
)


def build_agnt_with_tools_graph(
        tools: list[Tool], 
        invoke_llm_fn: Callable,
        state_type: Optional[Type] = GraphState, 
        agnt_name: Optional[str] = "agent"
):
    graph = StateGraph(state_type)

    tool_executor = ToolExecutor(tools)

    graph.add_node(agnt_name, invoke_llm_fn)
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
