#from scraper.scraper import main
from webapp.webapp import app
import uvicorn


if __name__ == "__main__":

    #main()
    uvicorn.run(app, host="0.0.0.0", port=8000)