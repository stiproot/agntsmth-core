import operator
from typing import (
    Sequence,
    TypedDict,
    Annotated,
    Annotated,
)
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    user_input: str
    global_messages: Annotated[Sequence[BaseMessage], operator.add]
    messages: Annotated[Sequence[BaseMessage], operator.add]


class C4ContextAgentState(AgentState):
    c4_context_diagram_path: str


class C4ContainerAgentState(AgentState):
    c4_context_diagram_path: str
    c4_container_diagram_path: str


class C4ComponentAgentState(AgentState):
    c4_container_diagram_path: str
    c4_component_diagram_path: str


class TaskTreeAgentState(AgentState):
    c4_component_diagram_path: str
    code_path: str


class RootState(TypedDict):
    user_input: str
    global_messages: Annotated[Sequence[BaseMessage], operator.add]
    c4_context_diagram_path: str
    c4_container_diagram_path: str
    c4_component_diagram_path: str
    code_path: str
