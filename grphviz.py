# coding=utf-8
from typing import Tuple

from contntprvdrs.strngprvdr import StringContentProvider
from contntprvdrs.epubprvdr import EpubContentProvider
from contntprvdrs.royalroad import RoyalRoadContentProvider
from contntprvdrs.txtfileprvdr import TextFileContentProvider

from contntprvdrs.wuxiaworld import WuxiaWorldContentProvider
from novelanalyze import infoextrct
from novelanalyze.contntprvdr import ContentProviderBase
from visual import grphnet

num_of_chapters_input_string = "Enter the number of chapters\n"
name_input_string = "Enter the novel's name\n"
url_input_string = "Enter the web novel's url\n"
file_path_input_string = "Enter the file path\n"


def extract_relations_graph(content_provider: ContentProviderBase):
    novel_entities = infoextrct.extract_entities(content_provider)
    grphnet.show_relations_network_graph(novel_entities)


def get_text_input_provider() -> ContentProviderBase:
    name = input(name_input_string)
    text = input("Please enter content\n")
    return StringContentProvider(name, text)


def get_text_file_provider() -> ContentProviderBase:
    file_path = input(file_path_input_string)
    return TextFileContentProvider(file_path)


def get_epub_file_provider() -> ContentProviderBase:
    file_path = input(file_path_input_string)
    num_of_chapters = input(num_of_chapters_input_string)
    return EpubContentProvider(file_path, int(num_of_chapters))


def get_royalroad_provider() -> ContentProviderBase:
    name = input(name_input_string)
    url = input(url_input_string)
    num_of_chapters = input(num_of_chapters_input_string)
    return RoyalRoadContentProvider(name, url, int(num_of_chapters))


remote_provider_tuples: Tuple[str, ContentProviderBase] = [
    ("Royalroad", RoyalRoadContentProvider),
    ("Wuxiaworld", WuxiaWorldContentProvider)
]


def get_remote_provider(provider_choice: int):
    name = input(name_input_string)
    url = input(url_input_string)
    num_of_chapters = int(input(num_of_chapters_input_string))
    provider_class = remote_provider_tuples[provider_choice - 1][1]
    return provider_class(name, url, num_of_chapters)


def get_prompt_string():
    prompt_string = \
        """Select the number of your wanted content provider:
        Local:
          1. Input text
          2. Text file
          3. Epub file
        Web crawl:
        """
    i = 3
    for remote_provider_tuple in remote_provider_tuples:
        prompt_string += f'{str(i)}. {remote_provider_tuple[0]}'
        i += 1
    return prompt_string


local_provider_getters = [get_text_input_provider, get_text_file_provider, get_epub_file_provider]

if __name__ == "__main__":
    provider_choice = int(input(get_prompt_string()))
    if provider_choice < 4:
        provider = local_provider_getters[provider_choice - 1]()
    else:
        provider = get_remote_provider(provider_choice - 3)
    extract_relations_graph(provider)
