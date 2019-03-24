from typing import List

from Analyzation.PostAnalysisProcessing.ObjectModel.CharacterData import Character


class Relationship:
    def __init__(self, character: Character):
        self.character = character
        self.total_sentiment_value = 0

    def add_sentiment(self, sentiment_value):
        self.total_sentiment += sentiment_value