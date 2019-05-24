# coding=utf-8
from contntprvdrs.string import StringContentProvider
from novelanalyze import infoextrct
from novelanalyze.contntprvdr import ContentProviderBase
from visual import grphnet


def extract_relations_graph(content_provider: ContentProviderBase):
    novel_entities = infoextrct.extract_entities(content_provider)
    grphnet.show_relations_network_graph(novel_entities)


if __name__ == "__main__":
    provider = StringContentProvider('test string', 'John is the father of Ron. John is the father of Bob')
    extract_relations_graph(provider)