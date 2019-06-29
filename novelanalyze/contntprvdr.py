# coding=utf-8
import itertools
import time
from abc import abstractmethod
from typing import Iterator


class ContentProviderBase:
    def __init__(self, novel_name: str, num_of_chapters: int):
        self.novel_name = novel_name
        self.num_of_chapters = num_of_chapters

    @abstractmethod
    def provide_chapter(self, indx_chapter: int) -> str:
        raise Exception('Unimplemented method')

    def generate_all_chapters(self) -> Iterator[str]:
        for indx_chapter in range(1, self.num_of_chapters):
            yield self.__delayed_provide_chapter(indx_chapter)

    def __delayed_provide_chapter(self, indx_chapter: int):
        time.sleep(1)
        return self.provide_chapter(indx_chapter)
