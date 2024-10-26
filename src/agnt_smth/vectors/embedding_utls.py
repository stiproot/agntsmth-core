import os
from typing import List, Dict, Awaitable
from langchain_core.tools import tool
from ..utls import log, traverse_folder

def embed_file_system_contents(file_system_path: str) -> Awaitable:
    """Embeds the contents of a file system into a dictionary.

    Args:
      file_system_path: The path to the file system to embed.

    Returns:
      Awaitable: an empty promise. 
    """

    log(f"embed_file_system_contents START. file_system_path: {file_system_path}")

    file_tree = traverse_folder(folder_path=file_system_path, ignore_folders=[".git", "__pycache__", "node_modules"])

