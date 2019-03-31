import itertools

from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.CharacterUpdater import CharacterNamedEntityUpdater
from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.LocationUpdater import LocationNamedEntityUpdater
from Analyzation.PostAnalysisProcessing.ObjectModels.BookData import BookData
from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.OrganizationUpdater import OrganizationNamedEntityUpdater
from Analyzation.TextAnalyzation.TextAnalysis import *

class TextAnalysisPostProcessor:
    def __init__(self):
        pass

    # update characters mentions based on current TextAnalysis
    # create relationships between characters
    def process_text_analysis(self, text_analysis: TextAnalysis, bookData: BookData, indx_chapter: int):

        CharacterNamedEntityUpdater().update(text_analysis, bookData.characters, indx_chapter)
        LocationNamedEntityUpdater().update(text_analysis, bookData.locations, indx_chapter)
        OrganizationNamedEntityUpdater().update(text_analysis, bookData.organizations, indx_chapter)

        named_entities = itertools.chain(bookData.characters, bookData.locations, bookData.organizations)

        RelationsProcessor.process(named_entities)
        CommonalitiesFinder.add_commonalities_relations(named_entities)





if __name__ == "__main__":
    pass
