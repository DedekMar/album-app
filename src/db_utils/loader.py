#from common.album import Album

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
#from db_utils.db import Session
import csv
from db_utils.db import Base, db_connect, create_albums_table



class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    sales = Column(Integer)
    cover_url = Column(String)
    rank_release_year = Column(Integer)
    rank_decade = Column(Integer)
    rank_overall = Column(Integer)

def load_data_from_csv(csv_filename):
    #session = Session()
    albumData = []
    with open(csv_filename, mode='r', encoding='utf-16') as csv_file:
        csvreader = csv.DictReader(csv_file, delimiter=',')


        for row in csvreader:
            #print(row)
            album = Album(
                title=row['title'],
                artist=row['artist'],
                sales=int(row['sales'].replace(',', '')),
                cover_url=row['cover_url'],
                rank_release_year=int(row['rank_release_year']),
                rank_decade=int(row['rank_decade']),
                rank_overall=int(row['rank_overall'])
            )
            albumData.append(album)

    #session.commit()
    #session.close()
    insert_album(albumData)

def insert_album(albumData):
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    #create_albums_table(engine)

    try:
        session.add_all(albumData)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    engine = db_connect()
    create_albums_table(engine)

    csv_filename = "album_data.csv"  # Replace with your CSV file path
    load_data_from_csv(csv_filename)