#from common.album import Album


from sqlalchemy.orm import sessionmaker
#from db_utils.db import Session
import csv
from db_utils.db import db_connect, create_albums_table, get_session_maker
from db_utils.models import AlbumModel



def load_data_from_csv(csv_filename):
    #session = Session()
    albumData = []
    with open(csv_filename, mode='r', encoding='utf-16') as csv_file:
        csvreader = csv.DictReader(csv_file, delimiter='\t')


        for row in csvreader:
            #print(row)
            album = AlbumModel(
                title=row['title'],
                artist=row['artist'],
                sales=int(row['sales'].replace(',', '')),
                cover_url=row['cover_url'],
                rank_release_year=int(row['rank_release_year']),
                rank_decade=int(row['rank_decade']),
                rank_overall=int(row['rank_overall']),
                release_year = int(row["release_year"]),
                album_scraped_id = int(row["album_scraped_id"]),
                artist_scraped_id = int(row["artist_scraped_id"])
            )
            albumData.append(album)

    #session.commit()
    #session.close()
    return albumData
    

class SomeClass:
    attribute : int
    def __init__(self, title):
        self.title = title


def insert_album(albumData):
    Session = get_session_maker()
    #create_albums_table(engine)

    # replaces the commit/rollback/close block with context manager
    with Session.begin() as session:
        session.add_all(albumData)    

def run_loader():
    engine = db_connect()
    create_albums_table(engine)

    csv_filename = "album_data.csv"  # Replace with your CSV file path
    albumData = load_data_from_csv(csv_filename)
    insert_album(albumData)

if __name__ == "__main__":
    run_loader()