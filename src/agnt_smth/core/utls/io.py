import os
from typing import List, Dict
from .logger_utls import log


def traverse_folder(
    folder_path: str, ignore_folders: List[str]
) -> Dict[str, List[str]]:

    log(f"traverse_folder START. folder_path: {folder_path}")

    file_dict = {}

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in ignore_folders]

        file_dict[root] = files

    log(f"traverse_folder END.")

    return file_dict
