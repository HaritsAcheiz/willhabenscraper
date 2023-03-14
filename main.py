from fastapi import FastAPI
from scraper import Scraper

s = Scraper()
app = FastAPI()

@app.get("/")
async def read_item():
    htmls = await s.run()
    return s.parser(htmls)