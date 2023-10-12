from db_utils.models import AlbumModel
from sqlalchemy.orm import Session

# from webapp.schemas import album_schema


def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AlbumModel).offset(skip).limit(limit).all()


def get_best_albums_in_year(db: Session, year: int, skip: int = 0, limit: int = 100):
    return (
        db.query(AlbumModel)
        .filter(AlbumModel.release_year == year)
        .order_by((AlbumModel.sales.desc()))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_album_by_id(db: Session, id: int):
    return db.query(AlbumModel).filter(AlbumModel.id == id).first()


def find_albums_by_title(db: Session, title: str, skip: int = 0, limit: int = 0):
    return (
        db.query(AlbumModel)
        .filter(AlbumModel.title.ilike(f"%{title}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )
