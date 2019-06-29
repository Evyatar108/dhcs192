# coding=utf-8
from contntprvdrs.chapterstring import StringContentProvider
from contntprvdrs.royalroad import RoyalRoadContentProvider
from novelanalyze import infoextrct
from novelanalyze.contntprvdr import ContentProviderBase
from visual import grphnet


def extract_relations_graph(content_provider: ContentProviderBase):
    novel_entities = infoextrct.extract_entities(content_provider)
    grphnet.show_relations_network_graph(novel_entities)


if __name__ == "__main__":
    #provider = StringContentProvider('THE STORY OF AN HOUR SUMMARY', '"I like baseball, and I like food"')
    provider = RoyalRoadContentProvider('dont-feed-the-dark', 'https://www.royalroad.com/fiction/6245/dont-feed-the-dark', 20)

    extract_relations_graph(provider)
