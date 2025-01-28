from typing import Awaitable
from ..core.utls import log, traverse_folder


async def embed_file_system_contents(file_system_path: str) -> Awaitable:
    """Embeds the contents of a file system.

    Args:
      file_system_path: The path to the file system to embed.

    Returns:
      Awaitable: an empty promise.
    """

    log(f"embed_file_system_contents START. file_system_path: {file_system_path}")

    file_tree = traverse_folder(
        folder_path=file_system_path,
        ignore_folders=[".git", "__pycache__", "node_modules", "bin", "obj"],
    )

    log(f"file_tree: {file_tree}")


async def embed_repo(repo_name: str, repo_target_dir: str) -> Awaitable:
    log(f"{embed_repo.__name__} START.")

    ignore_folders = ["node_modules", ".git", "bin", "obj", "__pycache__"]
    ignore_extensions = [
        ".pfx",
        ".crt",
        ".pem",
        ".postman_collection.json",
        ".postman_environment",
        ".png",
        ".gif",
        ".jpeg",
        ".jpg",
        ".ico",
        ".svg",
        ".woff",
        ".woff2",
        ".ttf",
        ".gz",
        ".zip",
        ".tar",
        ".tgz",
        ".tar.gz",
        ".rar",
        ".7z",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx"
    ]

    file_dict = traverse_folder(repo_target_dir, ignore_folders, ignore_extensions)
    file_paths = [f"{k}/{f}" for k, v in file_dict.items() for f in v]
    log(f"{embed_repo.__name__} -> file_paths: {file_paths}")

    chroma_client = ChromaHttpClientFactory.create_with_auth()
    embedding_function = EmbeddingFactory.create()

    chunk_embed_and_publish(
        file_paths=file_paths,
        collection_name=repo_name,
        embedding_function=embedding_function,
        chroma_client=chroma_client,
        chunk_size=4000,
        chunk_overlap=200,
    )

    log(f"{embed_repo.__name__} END.")
