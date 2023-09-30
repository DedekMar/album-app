from scraper import scraper
from webapp.webapp import app
from db_utils import loader
import uvicorn
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Web Scraping and Fast API demo")
    parser.add_argument("--scrape", action = "store_true", help="Run scraping script")
    parser.add_argument("--webapp", action = "store_true", help="Run webapp")
    parser.add_argument("--loader", action = "store_true", help="Run csv loader on scraped data")

    args = parser.parse_args()
    if args.scrape:
        print("scrape")
        scraper.main()
    if args.webapp:
        print("webapp")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    if args.loader:
        print("loader")
        loader.run_loader()
    #main()
    #