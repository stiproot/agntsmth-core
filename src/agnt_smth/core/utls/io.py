import os
from typing import List, Dict
from .logger_utls import log


def traverse_folder(
    folder_path: str, ignore_folders: List[str], ignore_extensions: List[str] = None
) -> Dict[str, List[str]]:

    log(f"{traverse_folder.__name__} START. folder_path: {folder_path}")

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

    log(f"{traverse_folder.__name__} END.")

    return file_dict
