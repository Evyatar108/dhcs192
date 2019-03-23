from typing import List

from Analyzation.PostAnalysisProcessing.CharacterData import Character


class Relationship:
    def __init__(self, first_character: Character, second_character: Character, sentiments: List[int]):
        self.first_character = first_character
        self.second_character = second_character
        self.sentiments = sentiments