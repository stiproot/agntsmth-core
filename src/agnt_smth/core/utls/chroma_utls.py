from typing import List
import chromadb
import uuid
import base64
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from .model_factory import EmbeddingFactory
from .env import EnvVarProvider

env = EnvVarProvider()


class ChromaHttpClientFactory:
    @staticmethod
    def create_with_auth_header():
        host = env.get_env_var("CHROMA_HOST", "localhost")
        port = env.get_env_var("CHROMA_PORT", 8000)
        usr = env.get_env_var("CHROMA_USR", "admin")
        pwd = env.get_env_var("CHROMA_PWD", "admin")

        auth_str = f"{usr}:{pwd}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_auth}"}

        chroma_client = chromadb.HttpClient(
            settings=Settings(allow_reset=True), host=host, port=port, headers=headers
        )

        return chroma_client


    @staticmethod
    def create_with_auth():
        host = env.get_env_var("CHROMA_HOST", "localhost")
        port = env.get_env_var("CHROMA_PORT", 8000)
        usr = env.get_env_var("CHROMA_USR", "admin")
        pwd = env.get_env_var("CHROMA_PWD", "admin")

        auth_str = f"{usr}:{pwd}"

        chroma_client = chromadb.HttpClient(
            settings=Settings(allow_reset=True, chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider", chroma_client_auth_credentials=auth_str), 
            host=host, 
            port=port
        )

        return chroma_client


    @staticmethod
    def create():
        host = env.get_env_var("CHROMA_HOST", "localhost")
        port = env.get_env_var("CHROMA_PORT", 8000)

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
    chunk_size: int = 1500,
    chunk_overlap: int = 50,
):
    vector_store = Chroma(
        embedding_function=embedding_function,
        client=chroma_client,
        collection_name=collection_name,
    )

    for file_path in file_paths:
        loader = TextLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        doc_splits = text_splitter.split_documents(docs)

        split_texts = [doc.page_content for doc in doc_splits]
        embeddings = embedding_function.embed_documents(split_texts)
        ids = [f"{file_path}_{i}" for i in range(len(embeddings))]

        if not len(ids):
            continue

        vector_store.add_documents(documents=doc_splits, embeddings=embeddings, ids=ids)


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
