import typing as tp
import aiofiles
import httpx
import pathlib

import uuid


class FileManager:
    __upload_dir: str

    def __init__(self, upload_dir: str) -> None:
        self.__upload_dir = upload_dir

    async def upload(self, filename: str, file: bytes) -> str:
        """Загружает файл и возвращает его название"""
        is_exists = self.__check_file_exists(filename)
        if is_exists:
            filename = self.__generate_unique_filename(filename)

        path = pathlib.Path(self.__upload_dir) / filename
        async with aiofiles.open(path, mode="wb") as _file:
            await _file.write(file)

        return filename

    async def read(self, file_name: str) -> bytes:
        file_path = f"{self.__upload_dir}/{file_name}"
        async with aiofiles.open(file_path, mode="rb") as file:
            content = await file.read()
            return content

    def __check_file_exists(self, filename: str) -> bool:
        path = pathlib.Path(self.__upload_dir) / filename
        return path.exists()

    def __generate_unique_filename(self, filename: str) -> str:
        name, ext = filename.split(".")
        name = str(uuid.uuid4())

        if len(name) > 251:  # len(ext) = 3; len(".") = 1 => len(name) = 255 - 4
            name = name[:251]

        return f"{name}.{ext}"
