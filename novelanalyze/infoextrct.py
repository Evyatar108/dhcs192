# coding=utf-8

from contntprvdrs.chapterstring import StringContentProvider
from novelanalyze.analyztn import corenlp, convert, enrich
from novelanalyze.analyztn.parsedata import TextAnalysis
from novelanalyze.contntprvdr import ContentProviderBase
from novelanalyze.prcssng.entitydata import NovelEntities
from novelanalyze.prcssng.insights import commonalities
from novelanalyze.prcssng.insights import relations
from novelanalyze.prcssng.insights import sharedrelations
from novelanalyze.prcssng.updtrs.char import CharacterNamedEntityUpdater
from novelanalyze.prcssng.updtrs.loc import LocationNamedEntityUpdater
from novelanalyze.prcssng.updtrs.org import OrganizationNamedEntityUpdater


def extract_entities(novel_content_provider: ContentProviderBase) -> NovelEntities:
    chapters_generator = novel_content_provider.generate_all_chapters()
    novel_entities = NovelEntities(novel_content_provider.novel_name)
    for indx_chapter, chapter in enumerate(chapters_generator):
        print(f'Analayzing chapter number {indx_chapter}')
        print(f'chapter: {chapter}')
        chapter = chapter.replace("’", "'")
        raw_data = corenlp.query_model(chapter)
        print(f'Queried model')
        enrich.improve_coreferences(raw_data)
        print('Improved coreferences')
        text_analysis = convert.convert_to_local_obj(raw_data)
        print('Converted to local object')
        __process_chapter_analysis(text_analysis, novel_entities, indx_chapter + 1)
        print('Processed chapter analysis')

    named_entities = list(novel_entities.get_named_entities())

    relations.process(named_entities)
    print('Processed relations')
    sharedrelations.process(named_entities)
    print('Processed shared relations')
    commonalities.process(named_entities)
    print('Processed commonalities')

    return novel_entities


def __process_chapter_analysis(text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    print('Updated character entities')
    LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    print('Updated location entities')
    OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)
    print('Updated organization entities')


if __name__ == "__main__":
    provider = StringContentProvider('test string', 'John is the father of Ron. John is the father of Bob')
    novel_entities = extract_entities(provider)
    pass
