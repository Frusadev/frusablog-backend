import os
import shutil

from fastapi import UploadFile

from app.config import env
from app.db.models import Media

STORAGE = env.get_env("STORAGE", "fs/storage")
os.makedirs(STORAGE, exist_ok=True)


def write_file(uploaded_file: UploadFile, media: Media):
    with open(f"{STORAGE}/{media.media_id}", "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)


def get_file(media: Media):
    with open(f"{STORAGE}/{media.media_id}", "rb") as buffer:
        return buffer.read()
