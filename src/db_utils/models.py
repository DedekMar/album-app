from db_utils.db import Base
from sqlalchemy import Column, Integer, String

class AlbumModel(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    sales = Column(Integer)
    cover_url = Column(String)
    rank_release_year = Column(Integer)
    rank_decade = Column(Integer)
    rank_overall = Column(Integer)