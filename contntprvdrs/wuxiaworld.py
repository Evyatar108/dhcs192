# coding=utf-8
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from novelanalyze.contntprvdr import ContentProviderBase

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


class WuxiaWorldContentProvider(ContentProviderBase):
    def __init__(self, name: str, url: str, num_of_chapters: int):
        super().__init__(name, num_of_chapters)
        uri = urlparse(url)

        self.host_name = f'{uri.scheme}://{uri.netloc}'
        self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

    def provide_chapter(self, indx_chapter: int) -> str:
        chapter_urls = [tag.select_one('a[href]')['href'] for tag in self.soup.find_all("li", class_="chapter-item")]
        if len(chapter_urls) > indx_chapter and f"chapter-{indx_chapter}" in chapter_urls[indx_chapter]:
            url = chapter_urls[indx_chapter]
        else:
            url = chapter_urls[indx_chapter - 1]
        paragraphs = BeautifulSoup(requests.get(self.host_name+url, headers=headers).content, 'html.parser')\
            .find("div", class_="fr-view")\
            .find_all('p')
        paragraphs_text = [paragraph.text for paragraph in paragraphs]
        return "\n".join(paragraphs_text)
