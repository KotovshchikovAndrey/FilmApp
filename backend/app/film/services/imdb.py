import typing as tp
import httpx

from app.core import config
from app.exceptions.api import ApiError


async def fetch_poster_url_by_imdb_id(imdb_id: str) -> tp.Optional[str]:
    url = f"http://api.themoviedb.org/3/movie/{imdb_id}/images?api_key={config.TMDB_API_KEY}"
    async with httpx.AsyncClient(timeout=1.2) as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                posters = response.json()["posters"]
                if posters:
                    return posters[0]["file_path"]
        except httpx.TimeoutException:
            return None


async def fetch_poster_binary_file(
    poster_url: str, poster_size: tp.Optional[int] = None
) -> tp.Optional[bytes]:
    if poster_size is None:
        poster_size = "original"
    else:
        poster_size = f"w{poster_size}"

    url = f"https://image.tmdb.org/t/p/{poster_size}{poster_url}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                poster = response.content
                return poster
        except httpx.TimeoutException:
            return None


async def fetch_trailer_by_imdb_id(imdb_id: str):
    ...
