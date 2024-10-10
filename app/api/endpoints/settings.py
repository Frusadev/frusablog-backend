import os

from dotenv import load_dotenv

load_dotenv(os.getcwd() + "/.env")


class EnvironmentError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


SECRET_KEY = os.getenv("secret")
ALGORITHM = os.getenv("algorithm")
ACCESS_TOKEN_EXPIRATION_TIME = 40  # In days

if not SECRET_KEY:
    raise EnvironmentError("Could not load SECRET_KEY")

if not ALGORITHM:
    raise EnvironmentError("Could not load ALGORITHM")
