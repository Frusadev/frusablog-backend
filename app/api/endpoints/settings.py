import os

from dotenv import load_dotenv

_ = load_dotenv()

SECRET_KEY = os.getenv("secret")
ALGORITHM = os.getenv("algorithm")
ACCESS_TOKEN_EXPIRATION_TIME = 40  # In days
if not SECRET_KEY:
    SECRET_KEY = "7a37f743415645aa80efd123ff83b4c9a13010e4e2561024959c421c428eb298"

if not ALGORITHM:
    ALGORITHM = "HS256"
