import operator
from typing import (
    Sequence,
    TypedDict,
    Annotated,
    Annotated,
)
from langchain_core.messages import BaseMessage


class GraphState(TypedDict):
    user_input: str
    global_message_history: Annotated[Sequence[BaseMessage], operator.add]
    message_history: Annotated[Sequence[BaseMessage], operator.add]


class C4ContextAgentState(GraphState):
    c4_context_diagram_path: str


class C4ContainerAgentState(GraphState):
    c4_context_diagram_path: str
    c4_container_diagram_path: str


class C4ComponentAgentState(GraphState):
    c4_container_diagram_path: str
    c4_component_diagram_path: str


class TaskTreeAgentState(GraphState):
    c4_component_diagram_path: str
    code_path: str


class RootState(TypedDict):
    user_input: str
    global_message_history: Annotated[Sequence[BaseMessage], operator.add]
    c4_context_diagram_path: str
    c4_container_diagram_path: str
    c4_component_diagram_path: str
    code_path: str
