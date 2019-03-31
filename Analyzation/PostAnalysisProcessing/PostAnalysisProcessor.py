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

        RelationsProcessor.process(bookData.characters, bookData.locations, char_loc_relations_rules)
        RelationsProcessor.process(bookData.characters, bookData.organizations, char_org_relations_rules)
        RelationsProcessor.process(bookData.organizations, bookData.locations, org_loc_relations_rules)

        CommonalitiesFinder.add_commonalities_relations(bookData.characters)
        CommonalitiesFinder.add_commonalities_relations(bookData.locations)
        CommonalitiesFinder.add_commonalities_relations(bookData.organizations)





if __name__ == "__main__":
    pass
