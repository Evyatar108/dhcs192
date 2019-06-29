# coding=utf-8
from novelanalyze.contntprvdr import ContentProviderBase


class StringContentProvider(ContentProviderBase):
    def __init__(self, novel_name: str, string: str):
        super().__init__(novel_name, 1)
        self.string = string

    def provide_chapter(self, indx_chapter: int) -> str:
        if indx_chapter == 1:
            return self.string
        return ''
