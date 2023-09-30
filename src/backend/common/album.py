from dataclasses import dataclass

@dataclass
class Album:
    title: str
    artist: str
    sales: int
    cover_url: str
    release_year: int
    rank_release_year: int
    rank_decade: int
    rank_overall: int
    album_scraped_id: int
    artist_scraped_id: int
