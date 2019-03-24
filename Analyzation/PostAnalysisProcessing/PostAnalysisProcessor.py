from Analyzation.PostAnalysisProcessing.CharacterUpdater import CharacterUpdater
from Analyzation.PostAnalysisProcessing.ObjectModel.RelationshipsData import Relationship
from Analyzation.TextAnalyzation.TextAnalysis import *
from Analyzation.PostAnalysisProcessing.ObjectModel.CharacterData import Character


class TextAnalysisPostProcessor:
    def __init__(self):
        pass

    # update characters mentions based on current TextAnalysis
    # create relationships between characters
    def process_text_analysis(self, text_analysis: TextAnalysis, characters: List[Character],
                              relationships: List[Relationship], indx_chapter: int):

        CharacterUpdater().update_characters_information(text_analysis, characters, indx_chapter)
        #LocationUpdater().
        #OrganizationUpdater






if __name__ == "__main__":
    pass
