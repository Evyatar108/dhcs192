from Analyzation.PostAnalysisProcessing.CharacterUpdater import CharacterUpdater
from Analyzation.PostAnalysisProcessing.RelationshipsData import Relationship
from Analyzation.PostAnalysisProcessing.RelationshipsUpdater import RelationshipsUpdater
from Analyzation.TextAnalyzation.TextAnalysis import *
from Analyzation.PostAnalysisProcessing.CharacterData import Character, Mentions


class TextAnalysisPostProcessor:
    def __init__(self):
        pass

    # update characters mentions based on current TextAnalysis
    # create relationships between characters
    def process_text_analysis(self, text_analysis: TextAnalysis, characters: List[Character],
                              relationships: List[Relationship], indx_chapter: int):
        charUpdater = CharacterUpdater()
        charUpdater.update_characters_information(text_analysis, charUpdater, indx_chapter)

        relationshipsUpdater = RelationshipsUpdater()
        relationshipsUpdater.update_relationships(text_analysis, characters, relationships)






if __name__ == "__main__":
    pass
