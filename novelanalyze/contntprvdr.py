# coding=utf-8
import itertools
import time
from abc import abstractmethod
from typing import Iterator


class ContentProviderBase:
    def __init__(self, novel_name: str):
        self.novel_name = novel_name

    @abstractmethod
    def provide_chapter(self, indx_chapter: int) -> str:
        raise Exception('Unimplemented method')

    def generate_all_chapters(self) -> Iterator[str]:
        #return [self.__delayed_provide_chapter(1)]
         return itertools.takewhile(lambda chapter: chapter != '',
                                    (self.provide_chapter(indx_chapter) for indx_chapter in
                                     itertools.count(start=1, step=1)))

    def __delayed_provide_chapter(self, indx_chapter: int):
        time.sleep(1)
        return self.provide_chapter(indx_chapter)
