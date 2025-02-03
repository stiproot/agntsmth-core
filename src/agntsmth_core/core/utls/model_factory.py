from typing import Optional, List
from pydantic import BaseModel
from langchain_core.tools import Tool
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import os

from .config_loader import load_openai_config

openai_config = load_openai_config()


class ModelFactory:
    @staticmethod
    def create(
        tools: Optional[List[Tool]] = None,
        structured_output_model: Optional[BaseModel] = None
    ):
        llm = AzureChatOpenAI(**openai_config)
        if tools:
            llm = llm.bind_tools(tools)
        if structured_output_model:
            llm = llm.with_structured_output(structured_output_model)
        return llm


class EmbeddingFactory:
    @staticmethod
    def create():
        azure_embedding = AzureOpenAIEmbeddings(
            deployment="text-embedding-ada-002",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        return azure_embedding
