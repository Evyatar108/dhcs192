import itertools

from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.character_updater import CharacterNamedEntityUpdater
from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.location_updater import LocationNamedEntityUpdater
from Analyzation.PostAnalysisProcessing.ObjectModels.novel_data import NovelEntities
from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.organization_updater import OrganizationNamedEntityUpdater
from Analyzation.TextAnalyzation.text_analysis import *


    # update characters mentions based on current TextAnalysis
    # create relationships between characters
def process_text_analysis(self, text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)

    named_entities = itertools.chain(novel_entities.characters, novel_entities.locations, novel_entities.organizations)

    RelationsProcessor.process(named_entities)
    CommonalitiesFinder.add_commonalities_relations(named_entities)





if __name__ == "__main__":
    pass
