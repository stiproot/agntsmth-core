import yaml
import json
from typing import Annotated, Type, Any, List, Dict
from pydantic import BaseModel, Field

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools import BaseTool
from langchain_core.vectorstores import VectorStoreRetriever

from ..utls import RetrieverFactory, log


class RetrieveAdditionalContextToolSchema(BaseModel):
    query: str = Field(description="The query to search for.")


class RetrieveAdditionalContextTool(BaseTool):
    """
    This tool queries a vectorstore for additional information.
    """

    name: str = "retrieve_additional_context"
    description: str = "Queries a vectorstore for additional information."
    args_schema: Type[BaseModel] = RetrieveAdditionalContextToolSchema
    retriever: Any = None

    def __init__(
        self,
        retriever: VectorStoreRetriever = None,
        /,
        **data: Any,
    ):
        """
        An agent tool for fetching addition context from a vectorstore.
        """

        super().__init__(**data)

        self.retriever = retriever
        if self.retriever is None:
            self.retriever = RetrieverFactory.create(collection_name=kwargs["collection_name"])

    def _run(self, query: str) -> str:
        """Use the tool"""
        log(f"{self.name}. START: query: {query}")
        resp = self.retriever.invoke(query)
        log(f"{self.name}. END: query: {query}")
        return resp

    async def _arun(self, query: str) -> str:
        """Use the tool"""
        return self._run(query)
