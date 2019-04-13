# coding=utf-8
from typing import Iterator

from novelanalyze.contntprvdr import ContentProviderBase


class WuxiaWorldContentProvider(ContentProviderBase):
    def __init__(self, url: str):
        self.url = url

    def provide_chapter(self, indx_chapter: int) -> str:
        pass

    def generate_all_chapters(self) -> Iterator[str]:
        pass