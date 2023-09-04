from os.path import basename
from typing import ByteString

import pytest
from dataclasses import dataclass
from pathlib import Path
import math

__all__ = [
    "binary_file",
    "read_file_from_disk"
]


@dataclass
class FileContract:
    name: str
    path: str
    type: str
    size: str


@dataclass
class FileBytesContract:
    name: str
    content: ByteString
    size: str


@pytest.fixture
def binary_file(read_file_from_disk):
    """Считывает файл с диска и возвращает название файла и биннарные данные файла."""
    def _file(path: str):
        file_name = basename(path)
        file_bytes, size = read_file_from_disk(path)
        return FileBytesContract(file_name, file_bytes, size)
    return _file


@pytest.fixture
def read_file_from_disk():
    def _read(path: str):
        import io
        size = f'{math.ceil(Path(path).stat().st_size/1024)}Кб'
        with open(path, 'rb') as f:
            file = io.BytesIO(f.read())
        return file.getvalue(), size
    return _read
