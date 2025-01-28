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

from ..utls import create_retriever, ChromaHttpClientFactory, log, EmbeddingFactory


class RetrieverFactory:

    @staticmethod
    def create(collection_name: str, /, **kwargs: Dict[str, Any]) -> VectorStoreRetriever:
        """
        A vector store retriever factory.
        """

        chroma_client = kwargs.get("chroma_client", None)
        if not chroma_client:
            chroma_client = ChromaHttpClientFactory.create()

        embedding_function = kwargs.get("embedding_function", None)
        if not embedding_function:
            embedding_function = EmbeddingFactory.create()

        retriever = create_retriever(
            collection_name=collection_name,
            chroma_client=chroma_client,
            embedding_function=embedding_function,
        )

        return retriever
