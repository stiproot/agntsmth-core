from environs import Env
from typing import Optional
from os import environ


class EnvVarProvider:
    def __init__(self):
        self._env = Env()
        self._env.read_env(".env")

    def get_env_var(self, key: str, default: Optional[str] = "") -> str:

        if key in environ:
            return environ[key]

        val = self._env(key)
        if val is None or val == "":
            return default

        return val
