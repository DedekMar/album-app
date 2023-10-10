from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel


class AlbumBase(BaseModel):
    title: str
    artist: str
    sales: int
    cover_url: str
    id: int

    class Config:
        orm_mode = True
