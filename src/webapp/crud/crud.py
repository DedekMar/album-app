from sqlalchemy.orm import Session

from db_utils.models import AlbumModel
from webapp.schemas import album_schema

def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AlbumModel).offset(skip).limit(limit).all()
