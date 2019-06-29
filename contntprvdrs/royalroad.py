# coding=utf-8
from novelanalyze.contntprvdr import ContentProviderBase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
headers = {
    'User-Agent': user_agent
}

# TODO: add to readme: need to have chrome driver


class RoyalRoadContentProvider(ContentProviderBase):
    def __init__(self, name: str, url: str, num_of_chapters: int):
        super().__init__(name)
        opts = Options()
        opts.add_argument('headless')
        opts.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome('./chromedriver', options=opts)
        driver.get(url)
        elem = driver.find_element_by_xpath('//*[@id="chapters_length"]/label/select/option[5]')
        elem.click()

        uri = urlparse(url)
        self.host_name = f'{uri.scheme}://{uri.netloc}'
        self.soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        self.num_of_chapters = num_of_chapters

    def provide_chapter(self, indx_chapter: int) -> str:
        if self.num_of_chapters > self.num_of_chapters:
            return ''
        chapter_urls = [tag['href'] for tag in self.soup.find("table", id="chapters").select('a[href]')]
        url = chapter_urls[indx_chapter-1]
        time.sleep(1)
        paragraphs = BeautifulSoup(requests.get(self.host_name + url, headers=headers).content, 'html.parser') \
            .find("div", class_="chapter-inner chapter-content") \
            .find_all('p')
        paragraphs_text = [paragraph.text for paragraph in paragraphs]
        return "\n".join(paragraphs_text)
