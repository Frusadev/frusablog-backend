import os

from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default_value: str) -> str:
    return os.getenv(name) or default_value
