from fastapi import FastAPI

from app.app import run_app
from app.db.setup import connect_db

app = FastAPI()

if __name__ == "__main__":
    connect_db()
    run_app()
