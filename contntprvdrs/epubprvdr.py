# coding=utf-8
from typing import List, Iterator

import epub
from bs4 import BeautifulSoup
from novelanalyze.contntprvdr import ContentProviderBase


class EpubContentProvider(ContentProviderBase):
    def provide_chapter(self, indx_chapter: int) -> str:
        if len(self.chapters) > indx_chapter:
            return self.chapters[indx_chapter]
        return ''

    def __init__(self, file_path):
        book = epub.open_epub(file_path)
        self.chapters = self.extract_chapters(book)

    @staticmethod
    def extract_chapters(book: epub.EpubFile) -> List[str]:
        chapters = []
        for item in book.opf.manifest.values():
            if 'html' in item.href and 'chap' in item.href:
                chapter_with_html = book.read_item(item)
                soup = BeautifulSoup(chapter_with_html, 'html.parser')
                chapter_text = soup.get_text()
                chapters.append(chapter_text)
        return chapters
