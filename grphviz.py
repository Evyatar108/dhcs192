# coding=utf-8
from contntprvdrs.chapterstring import StringContentProvider
from contntprvdrs.epubprvdr import EpubContentProvider
from contntprvdrs.royalroad import RoyalRoadContentProvider
from contntprvdrs.wuxiaworld import WuxiaWorldContentProvider
from novelanalyze import infoextrct
from novelanalyze.contntprvdr import ContentProviderBase
from visual import grphnet

num_of_chapters_input_string = "Please enter the number of chapters\n"
name_input_string = "Please enter name\n"
url_input_string = "Please enter the web novel's url\n"


def extract_relations_graph(content_provider: ContentProviderBase):
    novel_entities = infoextrct.extract_entities(content_provider)
    grphnet.show_relations_network_graph(novel_entities)


def get_raw_text_provider() -> ContentProviderBase:
    name = input(name_input_string)
    text = input("Please enter content\n")
    return StringContentProvider(name, text)


def get_epub_file_provider() -> ContentProviderBase:
    file_path = input("Please enter the file path\n")
    num_of_chapters = input(num_of_chapters_input_string)
    return EpubContentProvider(file_path, int(num_of_chapters))


def get_royalroad_provider() -> ContentProviderBase:
    name = input(name_input_string)
    url = input(url_input_string)
    num_of_chapters = input(num_of_chapters_input_string)
    return RoyalRoadContentProvider(name, url, int(num_of_chapters))


def get_wuxiaworld_provider() -> ContentProviderBase:
    name = input(name_input_string)
    url = input(url_input_string)
    num_of_chapters = input(num_of_chapters_input_string)
    return WuxiaWorldContentProvider(name, url, int(num_of_chapters))


if __name__ == "__main__":
    provider_num = input("""Please select the number of your wanted content provider:
local data:
  1. raw text
  2. epub file
web crawlers:
  3. royalroad
  4. wuxiaworld
""")
    provider_getters = [get_raw_text_provider, get_epub_file_provider, get_royalroad_provider, get_wuxiaworld_provider]
    provider = provider_getters[int(provider_num) - 1]()
    extract_relations_graph(provider)

