import sys
from abc import ABC, abstractmethod
import requests
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass
import pandas as pd
from urllib.parse import urlparse


@dataclass
class Album:
    title: str
    artist: str
    sales: int
    cover_url: str
    rank_release_year: int
    rank_decade: int
    rank_overall: int





class ScraperBase(ABC):

    @abstractmethod
    def run_scraper() -> list[Album]:
        pass
        

class ScraperSync(ScraperBase):

    def __init__(self, base_url : str, max_retries : int = 3, retry_interval : float = 5, between_req_wait : float = 5) -> None:
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.between_req_wait = between_req_wait 

    def _get_last_page_num(self):
        # Get last page number for pagination by finding the max value link
        response = self._get_response(self.base_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        page_items = soup.find_all(class_ = 'page_item')
        if not page_items:
            raise ValueError("No elements with class 'page_item' were found.")
        
        max_page_num = 0
        print("Finding last page")

        for page_item in page_items:
            link = page_item.find('a')
            if link:
                link_text = link.text.strip()
                if link_text.isdigit():
                    page_num = int(link_text)
                    max_page_num = page_num if page_num > max_page_num else max_page_num
        print(f"Last page is {max_page_num}")

        return max_page_num
    
    def _get_response(self, page_url : str):
        # try to get http response using requests with given paramteres
        retry_counter = 0
        exception = None
        print(f"Attempting connection to {page_url}. Max retries is {self.max_retries}")
        while retry_counter < self.max_retries:
            try:
                response = requests.get(page_url)
                response.raise_for_status()
                return response
            
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve page {page_url}, sleeping for {self.retry_interval}")
                retry_counter += 1
                time.sleep(self.retry_interval)
                exception = e
        raise exception #Exception(f"Failed to retrieve valid response for {page_url}: e")
    
    def _remove_relative_url_path(self, url : str) -> str:
        # extract the base domain from base_url then remove the relative path in url if exists and replace it with domain
        parsed_url = urlparse(self.base_url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        url = url.replace("..", domain) if ".." in url else url
        return url
    
    def _extract_album_card(self, album_card) -> Album:
        # extract all information from given album_card html tag
        rank = album_card.find(class_='rank').text.strip()
        cover_url = album_card.find(class_='pic')['src']
        cover_url = self._remove_relative_url_path(cover_url)
        album_info = album_card.find(class_='data_col')

        title = album_info.find(class_='album').find('a').text.strip()
        artist = album_info.find(class_='artist').find('a').text.strip()
        sales_text = album_info.find(class_='sales').text.strip()
        sales = int(sales_text.replace('Sales: ', '').replace(',', ''))

        ranks_row = album_info.find(class_='ranks_row')
        ranks = ranks_row.find_all(class_='ranks')

        rank_release_year = int(ranks[0].text.split(':')[-1].strip())
        rank_decade = int(ranks[1].text.split(':')[-1].strip())
        rank_overall = int(ranks[2].text.split(':')[-1].strip())

        # Create and return an Album instance
        album = Album(
            title=title,
            artist=artist,
            sales=sales,
            cover_url=cover_url,
            rank_release_year=rank_release_year,
            rank_decade=rank_decade,
            rank_overall=rank_overall,
        )
        return album



    def _scrape_page(self, page_url : str) -> list[Album]:
        # get all album_cards from given page
        response = self._get_response(page_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        album_cards = soup.find_all(class_='album_card')

        scraped_albums = []

        for album_card in album_cards:
            album = self._extract_album_card(album_card)
            scraped_albums.append(album)
        print(f"Scraped {len(scraped_albums)} albums from {page_url}")
        return scraped_albums


    def run_scraper(self) -> list[Album]:
        # run scraper for all pages in the base_url

        last_page = self._get_last_page_num()
        last_page = 4
        # first page doesnt work through URL param
        all_data = []

        page1_data = self._scrape_page(self.base_url)
        all_data.extend(page1_data)

        for page in range(2, last_page + 1 ):
            page_data = self._scrape_page(f'{self.base_url}-{page}')
            all_data.extend(page_data)
        
        return all_data




def main():
    base_url = "https://bestsellingalbums.org/decade/1980"
    scraper = ScraperSync(base_url= base_url)
    data = scraper.run_scraper()

    album_data_dicts = [album.__dict__ for album in data]
    df = pd.DataFrame(album_data_dicts)
    print(df)
    df.to_csv("album_data.csv", index=False)

if __name__ == ("__main__"):
    main()