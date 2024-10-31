from typing import Tuple
from langchain_core.tools import tool
import subprocess
from ..utls import log, exec_sh_cmd


@tool
def run_bash_cmd(cmd: str) -> Tuple[str, str]:
    """Runs a bash command.

    Args:
      cmd: The cmd to exectute.

    Returns:
      Tuple[str, str]: A tuple, with the first value being the output and the second the error, if there is one.
    """

    return exec_sh_cmd(cmd)
