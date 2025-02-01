import os
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .env import EnvVarProvider
# from .logger_utls import log


DEFAULT_CHUNK_SIZE = 1500
DEFAULT_CHUNK_OVERLAP = 50

env = EnvVarProvider()


def traverse_folder(
    folder_path: str, ignore_folders: List[str], ignore_extensions: List[str] = None
) -> Dict[str, List[str]]:

    # log(f"{traverse_folder.__name__} START. folder_path: {folder_path}")

    file_dict = {}

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in ignore_folders]

        if ignore_extensions:
            files = [
                f
                for f in files
                if not any(f.endswith(ext) for ext in ignore_extensions)
            ]

        file_dict[root] = files

    # log(f"{traverse_folder.__name__} END.")

    return file_dict


def chunk_files(
    file_paths: List[str],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
) -> Dict[str, Dict[str, Any]]:
    chunk_size = chunk_size or env.get_env_var("CHUNK_SIZE", DEFAULT_CHUNK_SIZE)
    chunk_overlap = chunk_overlap or env.get_env_var("CHUNK_OVERLAP", DEFAULT_CHUNK_OVERLAP)

    chunk_hash = {}

    for file_path in file_paths:
        loader = TextLoader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        split_docs = text_splitter.split_documents(docs)
        split_texts = [doc.page_content for doc in split_docs]

        if not len(split_texts):
            continue

        chunk_hash[file_path] = {"split_docs": split_docs, "split_texts": split_texts}

    return chunk_hash
