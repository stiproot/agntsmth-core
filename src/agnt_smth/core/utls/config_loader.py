from typing import Optional
from json import load as json_load
import os
from .env import EnvVarProvider


DEFAULT_CONFIG_FILE_PATH = ".config/openai_config.json"
env = EnvVarProvider()


def load_openai_config(config_file_path: Optional[str] = None):
    if config_file_path is None:
        config_file_path = env.get_env_var("CONFIG_PATH", DEFAULT_CONFIG_FILE_PATH)

    with open(config_file_path) as f:
        openai_config = json_load(f)
        os.environ["AZURE_OPENAI_API_KEY"] = openai_config["openai_api_key"]
        os.environ["AZURE_OPENAI_ENDPOINT"] = openai_config["azure_endpoint"]
        os.environ["AZURE_OPENAI_API_VERSION"] = openai_config["openai_api_version"]
        return openai_config
