import typing as tp
import asyncio
import httpx
from pprint import pprint

from app.core import config
from film.utils.file_uploader import FileUploader


async def fetch_poster_url_by_imdb_id(imdb_id: str) -> str:
    url = f"https://imdb-api.com/en/API/Posters/k_o6916rfc/{imdb_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            posters = response.json()["posters"]
            if posters:
                return posters[0]["link"]


async def fetch_trailer_by_imdb_id(imdb_id: str):
    ...


# async def main():
#     poster = await fetch_poster_by_imdb_id("tt0114709")
#     file_uploader = FileUploader(upload_dir=config.UPLOAD_DIR + "/posters")
#     print("run upload")
#     await file_uploader.upload(file_url=poster, file_name="test")


# asyncio.run(main())
