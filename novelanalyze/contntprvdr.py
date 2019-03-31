import itertools
from typing import Generator


class ContentProviderBase:
    def provide_chapter(self, indx_chapter: int) -> str:
        raise Exception('Unimplemented method')

    def generate_all_chapters(self) -> Generator[str]:
        itertools.takewhile(lambda chapter: chapter,
                            (self.ProvideChapter(indx_chapter) for indx_chapter in itertools.count(start=1, step=1)))
