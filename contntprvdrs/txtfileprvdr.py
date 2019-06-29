# coding=utf-8
import os

from novelanalyze.contntprvdr import ContentProviderBase


class TextFileContentProvider(ContentProviderBase):
    def __init__(self, file_path: str):
        path, file_name = os.path.split(file_path)
        super().__init__(file_name, 1)
        self.file_path = file_path

    def provide_chapter(self, indx_chapter: int) -> str:
        file = open(self.file_path)
        return file.read()
