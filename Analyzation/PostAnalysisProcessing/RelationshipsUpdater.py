from typing import List

from Analyzation.PostAnalysisProcessing.CharacterData import Character
from Analyzation.PostAnalysisProcessing.RelationshipsData import Relationship
from Analyzation.TextAnalyzation.TextAnalysis import SentimentedSentence


class RelationshipsUpdater:

    def update_relationships(self, characters: List[Character], relationships: List[Relationship], sentences: List[SentimentedSentence]):
        for indx_character, character in enumerate(characters):

