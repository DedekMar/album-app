from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
#from db_utils.db import SessionLocal
from db_utils.models import AlbumModel
from db_utils import db as database
import uvicorn
from webapp.schemas import album_schema
from webapp.crud import crud


app = FastAPI()


origins = ["http://localhost", "http://127.0.0.1:5173", "http://localhost:5173"]  # Replace with your frontend URLs

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = database.get_session(autocommit=False, autoflush=False)
    try:
        yield db
    finally:
        db.close()



@app.get("/albums/", response_model= list[album_schema.AlbumBase])
def read_albums(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    limit = min(limit, 100)
    albums = crud.get_albums(db = db, skip = skip, limit = limit)
    return albums

@app.get("/albums/year/", response_model= list[album_schema.AlbumBase])
def read_albums_by_year(year : int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    limit = min(limit, 100)
    albums = crud.get_best_albums_in_year(db = db, year = year,  skip = skip, limit = limit)
    return albums
