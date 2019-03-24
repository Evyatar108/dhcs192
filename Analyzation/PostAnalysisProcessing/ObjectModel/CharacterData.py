from typing import Dict, List

from Analyzation.PostAnalysisProcessing.ObjectModel.MentionsData import Mentions
from Analyzation.PostAnalysisProcessing.ObjectModel.NamedEntityData import NamedEntity
from Analyzation.PostAnalysisProcessing.ObjectModel.RelationData import ExtendedRelation
from Analyzation.PostAnalysisProcessing.ObjectModel.RelationshipsData import Relationship


class Character(NamedEntity):
    def __init__(self, indx: int, names: List[str] =[], chapters_mentions: Dict[int, Mentions] = {},
                 relations_as_subject: List[ExtendedRelation]=[], relations_as_object: List[ExtendedRelation]=[],
                 gender="UNKNOWN", chapters_relationships: Dict[int, Dict[int, Relationship]] = {}):
        super().__init__(names, chapters_mentions, relations_as_subject, relations_as_object)
        self.indx = indx
        self.gender = gender
        self.chapters_relationships = chapters_relationships

    def add_relationship_sentiment(self, character, sentiment_value: int, indx_chapter: int):
        chapter_relationships = self.chapters_relationships.setdefault(indx_chapter, {})
        relationship: Relationship = chapter_relationships.setdefault(character.indx, Relationship(character))
        relationship.add_sentiment(sentiment_value)
