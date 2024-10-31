from typing import Tuple
from langchain_core.tools import tool
import subprocess
from .logger_utls import log


def exec_sh_cmd(cmd: str) -> Tuple[str, str]:
    """Executes a bash command.

    Args:
      cmd: The command to exectute.

    Returns:
      Tuple[str, str]: A tuple, with the first value being the output and the second the error, if there is one.
    """

    log(f"{exec_sh_cmd.__name__} START. cmd: {cmd}.")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = result.stdout.decode("utf-8").strip()
        err = result.stderr.decode("utf-8").strip()

        log(f"{exec_sh_cmd.__name__} END.")

        return output, err
    except subprocess.CalledProcessError as e:
        log(f"{exec_sh_cmd.__name__} ERROR. cmd: {cmd}, error: {str(e)}")
        return None, str(e)
