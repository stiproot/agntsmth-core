from typing import Dict, Any, List
import chromadb
import uuid
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from ..utls import (
    chunk_embed_and_publish,
    create_retriever,
    ChromaHttpClientFactory,
    EmbeddingFactory,
)


def init_chroma_client_data(file_data_hash: Dict[str, List[str]]):

    chroma_client = ChromaHttpClientFactory.create()
    azure_embedding = EmbeddingFactory.create()

    for collection_name, file_paths in file_data_hash.items():

        chunk_embed_and_publish(
            file_paths=file_paths,
            collection_name=collection_name,
            embedding_function=azure_embedding,
            chroma_client=chroma_client,
        )
