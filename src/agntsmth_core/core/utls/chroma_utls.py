from typing import List, Optional
import chromadb
import uuid
import base64
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .model_factory import EmbeddingFactory
from .env import EnvVarProvider
from .io import chunk_files


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000
DEFAULT_USR = "admin"
DEFAULT_PWD = "admin"
DEFAULT_CHUNK_SIZE = 1500
DEFAULT_CHUNK_OVERLAP = 50

env = EnvVarProvider()


class ChromaHttpClientFactory:
    @staticmethod
    def create_with_auth_header():
        host = env.get_env_var("CHROMA_HOST", DEFAULT_HOST)
        port = env.get_env_var("CHROMA_PORT", DEFAULT_PORT)
        usr = env.get_env_var("CHROMA_USR", DEFAULT_USR)
        pwd = env.get_env_var("CHROMA_PWD", DEFAULT_PWD)

        auth_str = f"{usr}:{pwd}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_auth}"}

        chroma_client = chromadb.HttpClient(
            settings=Settings(allow_reset=True), host=host, port=port, headers=headers
        )

        return chroma_client


    @staticmethod
    def create_with_auth():
        host = env.get_env_var("CHROMA_HOST", DEFAULT_HOST)
        port = env.get_env_var("CHROMA_PORT", DEFAULT_PORT)
        usr = env.get_env_var("CHROMA_USR", DEFAULT_USR)
        pwd = env.get_env_var("CHROMA_PWD", DEFAULT_PWD)

        auth_str = f"{usr}:{pwd}"

        chroma_client = chromadb.HttpClient(
            settings=Settings(allow_reset=True, chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider", chroma_client_auth_credentials=auth_str), 
            host=host, 
            port=port
        )

        return chroma_client


    @staticmethod
    def create():
        host = env.get_env_var("CHROMA_HOST", DEFAULT_HOST)
        port = env.get_env_var("CHROMA_PORT", DEFAULT_PORT)

        chroma_client = chromadb.HttpClient(
            settings=Settings(allow_reset=True), host=host, port=port
        )

        return chroma_client


def embed_and_publish(file_paths, collection_name):
    documents = []
    collection = chroma_client.create_collection(collection_name)

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            embedding = azure_embedding.embed_documents([content])[0]
            documents.append(
                {
                    "id": file_path,
                    "text": content,
                    "embedding": embedding,
                }
            )

    collection.add(documents=documents)


def chunk_embed_and_publish(
    file_paths: List[str],
    collection_name: str,
    embedding_function: AzureOpenAIEmbeddings,
    chroma_client: chromadb.HttpClient,
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
):
    chunk_size = chunk_size or env.get_env_var("CHUNK_SIZE", DEFAULT_CHUNK_SIZE)
    chunk_overlap = chunk_overlap or env.get_env_var("CHUNK_OVERLAP", DEFAULT_CHUNK_OVERLAP)

    vector_store = Chroma(
        embedding_function=embedding_function,
        client=chroma_client,
        collection_name=collection_name,
    )

    chunked_file_hash = chunk_files(file_paths, chunk_size, chunk_overlap)

    for file_path in chunked_file_hash:

        split_docs = chunked_file_hash[file_path]["split_docs"]
        split_texts = chunked_file_hash[file_path]["split_texts"]

        embeddings = embedding_function.embed_documents(split_texts)
        ids = [f"{file_path}_{i}" for i in range(len(embeddings))]

        if not len(ids):
            continue

        vector_store.add_documents(documents=split_docs, embeddings=embeddings, ids=ids)


def create_retriever(
    collection_name: str, chroma_client: chromadb.HttpClient, embedding_function: AzureOpenAIEmbeddings
):
    vector_store = Chroma(
        embedding_function=embedding_function,
        collection_name=collection_name,
        client=chroma_client,
    )

    # retriever = vector_store.as_retriever(
    #     search_type="similarity", search_kwargs={"k": 5}
    # )
    retriever = vector_store.as_retriever()

    return retriever
