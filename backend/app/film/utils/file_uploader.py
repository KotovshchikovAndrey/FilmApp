import typing as tp
import httpx
import pathlib


class FileUploader:
    __upload_dir: str

    def __init__(self, upload_dir: str) -> None:
        self.__upload_dir = upload_dir

    async def upload(self, file_url: str, file_name: str):
        upload_path = pathlib.Path(self.__upload_dir) / f"{file_name}.jpg"
        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            upload_path.write_bytes(response.content)

        return file_name
