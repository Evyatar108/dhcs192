# coding=utf-8
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from novelanalyze.contntprvdr import ContentProviderBase


class WuxiaWorldContentProvider(ContentProviderBase):
    def __init__(self, url: str):
        uri = urlparse(url)
        self.host_name = f'{uri.scheme}://{uri.netloc}'
        self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    def provide_chapter(self, indx_chapter: int) -> str:
        chapter_urls = [tag.select_one('a[href]')['href'] for tag in self.soup.find_all("li", class_="chapter-item")]
        if len(chapter_urls) > indx_chapter and f"chapter-{indx_chapter}" in chapter_urls[indx_chapter]:
            url = chapter_urls[indx_chapter]
        else:
            url = chapter_urls[indx_chapter - 1]
        paragraphs = BeautifulSoup(requests.get(self.host_name+url).content, 'html.parser')\
            .find("div", class_="fr-view")\
            .find_all('p')
        paragraphs_text = [paragraph.text for paragraph in paragraphs]
        return "\n".join(paragraphs_text)
