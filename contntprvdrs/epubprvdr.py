# coding=utf-8
import os
from typing import List

import epub
from bs4 import BeautifulSoup
from novelanalyze.contntprvdr import ContentProviderBase


class EpubContentProvider(ContentProviderBase):
    def __init__(self, file_path: str, num_of_chapters: int):
        self.num_of_chapters = num_of_chapters
        path, file_name = os.path.split(file_path)
        super().__init__(file_name, num_of_chapters)

        book = epub.open_epub(file_path)
        self.chapters = self.extract_chapters(book)

    def provide_chapter(self, indx_chapter: int) -> str:
        if len(self.chapters) > indx_chapter:
            return self.chapters[indx_chapter]
        return ''

    def extract_chapters(self, book: epub.EpubFile) -> List[str]:
        chapters = []
        parsed_chapters = 0
        for item in book.opf.manifest.values():
            if 'html' in item.href and 'chap' in item.href:
                chapter_with_html = book.read_item(item)
                soup = BeautifulSoup(chapter_with_html, 'html.parser')
                chapter_text = soup.get_text()
                chapters.append(chapter_text)
                parsed_chapters += 1
                if parsed_chapters >= self.num_of_chapters:
                    return chapters
        return chapters
