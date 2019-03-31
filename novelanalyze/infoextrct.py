import itertools

from novelanalyze.analyztn.data import TextAnalysis
from novelanalyze.contntprvdr import ContentProviderBase
from novelanalyze.analyztn import corenlp
from novelanalyze.prcssng.data.novel import NovelEntities
from novelanalyze.prcssng.updtrs.char import CharacterNamedEntityUpdater
from novelanalyze.prcssng.updtrs.loc import LocationNamedEntityUpdater
from novelanalyze.prcssng.updtrs.org import OrganizationNamedEntityUpdater


def extract(novel_content_provider: ContentProviderBase) -> NovelEntities:
    chapters_generator = novel_content_provider.generate_all_chapters()
    novel_entities = NovelEntities()
    for indx_chapter, chapter in enumerate(chapters_generator):
        text_analysis = corenlp.analyze(chapter)
        __process_chapter_analysis(text_analysis, novel_entities, indx_chapter)
    return novel_entities


def __process_chapter_analysis(text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)

    named_entities = itertools.chain(novel_entities.characters, novel_entities.locations, novel_entities.organizations)

    RelationsProcessor.process(named_entities)
    CommonalitiesFinder.add_commonalities_relations(named_entities)


if __name__ == '__main__':
    # todo add an example from offline/online novel
    pass
