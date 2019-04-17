# coding=utf-8
from itertools import chain

from novelanalyze.analyztn.parsedata import TextAnalysis
from novelanalyze.contntprvdr import ContentProviderBase
from novelanalyze.analyztn import corenlp, convert, enrich
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
        raw_data = corenlp.query_model(chapter)
        enrich.improve_coreferences(raw_data)
        text_analysis = convert.convert_to_local_obj(raw_data)
        __process_chapter_analysis(text_analysis, novel_entities, indx_chapter)

    named_entities = list(novel_entities.get_named_entities())

    relations.process(named_entities)
    sharedrelations.process(named_entities)
    commonalities.process(named_entities)

    return novel_entities


def __process_chapter_analysis(text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)


# todo add an example from offline/online novel
if __name__ == "__main__":
    example_sentence = 'Ron and John are good. They are nice, and he is strong'
    print('Executing Text Analysis')
    raw_data = corenlp.query_model(example_sentence)
    print('Finished Text Analysis')
    text_analysis = convert.convert_to_local_obj(raw_data)
    print('Converting Text Analysis to local object')
    pass
