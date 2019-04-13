# coding=utf-8
import itertools

from novelanalyze.analyztn.parsedata import TextAnalysis
from novelanalyze.contntprvdr import ContentProviderBase
from novelanalyze.analyztn import corenlp
from novelanalyze.prcssng.entitydata import NovelEntities
from novelanalyze.prcssng.updtrs.char import CharacterNamedEntityUpdater
from novelanalyze.prcssng.updtrs.loc import LocationNamedEntityUpdater
from novelanalyze.prcssng.updtrs.org import OrganizationNamedEntityUpdater
from novelanalyze.prcssng.insights import relations
from novelanalyze.prcssng.insights import sharedrelations
from novelanalyze.prcssng.insights import commonalities


def extract(novel_content_provider: ContentProviderBase) -> NovelEntities:
    chapters_generator = novel_content_provider.generate_all_chapters()
    novel_entities = NovelEntities()
    for indx_chapter, chapter in enumerate(chapters_generator):
        text_analysis, raw_data = corenlp.analyze(chapter)
        __process_chapter_analysis(text_analysis, novel_entities, indx_chapter)
    return novel_entities


def __process_chapter_analysis(text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)

    named_entities = itertools.chain(novel_entities.characters, novel_entities.locations, novel_entities.organizations)

    relations.process(named_entities)
    sharedrelations.process(named_entities)
    commonalities.process(named_entities)


if __name__ == '__main__':
    # todo add an example from offline/online novel
    pass
