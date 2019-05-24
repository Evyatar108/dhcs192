# coding=utf-8
from novelanalyze.contntprvdr import ContentProviderBase


class StringContentProvider(ContentProviderBase):
    def __init__(self, name: str, string: str):
        super().__init__(name)
        self.string = string

    def provide_chapter(self, indx_chapter: int) -> str:
        if indx_chapter == 1:
            return self.string
        return ''
