import typing as tp
import aiofiles
import httpx
import pathlib


class FileManager:
    __upload_dir: str

    def __init__(self, upload_dir: str) -> None:
        self.__upload_dir = upload_dir

    # async def upload(self, file: bytes):
    #     upload_path = pathlib.Path(self.__upload_dir) / f"{file_name}.jpg"
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(file_url)
    #         upload_path.write_bytes(response.content)

    #     return file_name

    async def read(self, file_name: str) -> bytes:
        file_path = f"{self.__upload_dir}/{file_name}"
        async with aiofiles.open(file_path, mode="rb") as file:
            content = await file.read()
            return content
