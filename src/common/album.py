from dataclasses import dataclass

@dataclass
class Album:
    title: str
    artist: str
    sales: int
    cover_url: str
    rank_release_year: int
    rank_decade: int
    rank_overall: int
