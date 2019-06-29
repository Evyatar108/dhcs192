# coding=utf-8
from typing import List

from contntprvdrs.strngprvdr import StringContentProvider
from novelanalyze.analyztn import corenlp, convert, enrich
from novelanalyze.analyztn.parsedata import TextAnalysis
from novelanalyze.contntprvdr import ContentProviderBase
from novelanalyze.prcssng.entitydata import NovelEntities, NamedEntity, Character, Location, Organization
from novelanalyze.prcssng.insights import commonalities, speaker
from novelanalyze.prcssng.insights import relations
from novelanalyze.prcssng.insights import sharedrelations
from novelanalyze.prcssng.updtrs.char import CharacterNamedEntityUpdater


def extract_entities(novel_content_provider: ContentProviderBase) -> NovelEntities:
    chapters_generator = novel_content_provider.generate_all_chapters()
    novel_entities = NovelEntities(novel_content_provider.novel_name)
    for indx_chapter, chapter in enumerate(chapters_generator):
        print(f'Analayzing chapter number {indx_chapter + 1}')
        chapter = chapter.replace("’", "'")
        print(f'Quering corenlp model')
        raw_data = corenlp.query_model(chapter)
        print('Improving coreferences')
        enrich.improve_coreferences(raw_data)
        print('Converting to local object')
        text_analysis = convert.convert_to_local_obj(raw_data)
        print('Processing and aggregating chapter analysis')
        __process_chapter_analysis(text_analysis, novel_entities, indx_chapter + 1)

    named_entities = list(novel_entities.get_named_entities())

    print('Inferring relations using regex')
    relations.process(named_entities)

    print('Merging speaker entities')
    speaker.process(named_entities)

    print('Inferring relations based on relations belonging to multiple entities')
    sharedrelations.process(named_entities)

    print('Inferring relations based on indirect relations')
    commonalities.process(named_entities)

    __update_novel_entities(novel_entities, named_entities)

    return novel_entities


def __process_chapter_analysis(text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    print('Processing character entities')
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    # LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    # print('Updated location entities')
    # OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)
    # print('Updated organization entities')


def __update_novel_entities(novel_entities: NovelEntities, named_entities: List[NamedEntity]):
    novel_entities.characters = [named_entity for named_entity in named_entities if isinstance(named_entity, Character)]
    novel_entities.locations = [named_entity for named_entity in named_entities if isinstance(named_entity, Location)]
    novel_entities.organizations = [named_entity for named_entity in named_entities if
                                    isinstance(named_entity, Organization)]


if __name__ == "__main__":
    provider = StringContentProvider('test string', 'I like to ski. John doesn\'t like to ski. I don\'t like John')
    novel_entities = extract_entities(provider)
    pass
