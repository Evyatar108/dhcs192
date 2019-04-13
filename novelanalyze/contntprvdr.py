# coding=utf-8
import itertools
from abc import abstractmethod
from typing import Iterator


class ContentProviderBase:
    @abstractmethod
    def provide_chapter(self, indx_chapter: int) -> str:
        raise Exception('Unimplemented method')

    @abstractmethod
    def generate_all_chapters(self) -> Iterator[str]:
        return itertools.takewhile(lambda chapter: chapter, (self.provide_chapter(indx_chapter) for indx_chapter in
                                                             itertools.count(start=1, step=1)))
