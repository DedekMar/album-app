import sys
import os
from pathlib import Path
from abc import ABC, abstractmethod
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import asyncio

#print (sys.path)
from common.album import Album

class ScraperBase(ABC):

    @abstractmethod
    def run_scraper() -> list[Album]:
        pass

    def _extract_last_page(self, response):
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
        album_scraped_id = int(album_info.find(class_='album').find('a')["href"].split('/')[-1])
        artist = album_info.find(class_='artist').find('a').text.strip()
        artist_scraped_id = int(album_info.find(class_='artist').find('a')["href"].split('/')[-1])
        sales_text = album_info.find(class_='sales').text.strip()
        sales = int(sales_text.replace('Sales: ', '').replace(',', ''))

        ranks_row = album_info.find(class_='ranks_row')
        ranks = ranks_row.find_all(class_='ranks')

        rank_release_year = int(ranks[0].text.split(':')[-1].strip())
        release_year_a = ranks[0].find("a")
        release_year = int(release_year_a["href"].split('/')[-1])
        rank_decade = int(ranks[1].text.split(':')[-1].strip())
        rank_overall = int(ranks[2].text.split(':')[-1].strip())


        # Create and return an Album instance
        album = Album(
            title=title,
            artist=artist,
            sales=sales,
            cover_url=cover_url,
            release_year=release_year,
            rank_release_year=rank_release_year,
            rank_decade=rank_decade,
            rank_overall=rank_overall,
            artist_scraped_id=artist_scraped_id,
            album_scraped_id=album_scraped_id
        )
        return album        
        
    def _extract_scraped_albums(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')

        album_cards = soup.find_all(class_='album_card')

        scraped_albums = []

        for album_card in album_cards:
            album = self._extract_album_card(album_card)
            scraped_albums.append(album)

        return scraped_albums


class ScraperAsync(ScraperBase):
    def __init__(self, base_url : str, max_retries : int = 3, retry_interval : float = 5, between_req_wait : float = 5, semaphore : int = 5) -> None:
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.between_req_wait = between_req_wait 
        self.semaphore = semaphore


    async def _get_last_page_number(self) -> int:
        # Extracts and returns the last page number from the website's pagination.
        response = await self._get_response(self.base_url)
        return self._extract_last_page(response)
    
    async def _get_response(self, page_url : str):
        # Sends a GET request to the specified 'page_url' and handles retries according to the 'max_retries' and 'retry_interval' specified during object creation.
        retry_counter = 0
        exception = None
        while retry_counter < self.max_retries:
            try:
                #async with self.semaphore:
                    response = await asyncio.to_thread(requests.get, page_url)
                    response.raise_for_status()  
                    return response
            except asyncio.CancelledError as e:
                # This exception occurs if the coroutine is canceled (e.g., due to a timeout)
                print(e)
                print(f"Coroutine for {page_url} was canceled due to timeout.")         
            except requests.exceptions.RequestException as e:
                retry_counter += 1                
                if response.status_code == 429:
                    # Implement exponential backoff
                    wait_time = 2 ** retry_counter
                    print(f"Received 429 error for {page_url}. Retrying in {wait_time} seconds.")
                    await asyncio.sleep(wait_time)
                else:
                    exception = e
                    await asyncio.sleep(self.between_req_wait)
        raise exception #Exception(f"Failed to retrieve valid response for {page_url}: e")
    

    async def scrape_page(self, page_url : str) -> list[Album]:
        """
        Scrapes content from a specific page URL and returns a list of results.

        Args:
            page_url (str): The URL of the page to be scraped.

        Returns:
            list: A list of tuples containing scraped data (title, summary, URL, image URL) from the page.
        """
        semaphore = asyncio.Semaphore(self.semaphore)
        async with semaphore:
            print(f'Scraping {page_url}')
            response = await self._get_response(page_url)
            print(f'Scraped {page_url}')
        

        return self._extract_scraped_albums(response)
    

    def run_scraper(self) -> list[Album]:
        return asyncio.run(self._run_scraper_async())
    
    async def _run_scraper_async(self) -> list[Album]:

        last_page = await self._get_last_page_number()
        #last_page = 10
        all_data = []
        # first page doesnt work through URL param
        # Scrape the first page separately as it has a different URL
        page1_task = self.scrape_page(self.base_url)


        # Use asyncio.gather to concurrently scrape the remaining pages
        tasks = [page1_task] + [self.scrape_page(f'{self.base_url}-{page}') for page in range(2, last_page + 1)]
        results = await asyncio.gather(*tasks)
        for page_result in results:
            all_data.extend(page_result)

        return all_data


class ScraperSync(ScraperBase):

    def __init__(self, base_url : str, max_retries : int = 3, retry_interval : float = 5, between_req_wait : float = 5) -> None:
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.between_req_wait = between_req_wait 

    def _get_last_page_num(self):
        # Get last page number for pagination by finding the max value link
        response = self._get_response(self.base_url)
        last_page = self._extract_last_page(response)

        return last_page
    
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
        


    def _scrape_page(self, page_url : str) -> list[Album]:
        # get all album_cards from given page
        response = self._get_response(page_url)

        scraped_albums = self._extract_scraped_albums(response)
        print(f"Scraped {len(scraped_albums)} albums from {page_url}")
        return scraped_albums


    def run_scraper(self) -> list[Album]:
        # run scraper for all pages in the base_url

        last_page = self._get_last_page_num()
        #last_page = 2
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
    scraper = ScraperAsync(base_url= base_url)
    data = scraper.run_scraper()

    album_data_dicts = [album.__dict__ for album in data]
    df = pd.DataFrame(album_data_dicts)
    print(df)
    df.to_csv("album_data.csv", encoding = "UTF-16", index=False, sep='\t')

if __name__ == ("__main__"):
    main()