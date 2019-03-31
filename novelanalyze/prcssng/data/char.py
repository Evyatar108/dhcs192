from typing import Dict, List
from __future__ import annotations

from novelanalyze.prcssng.data.entity import NamedEntity, ExtendedRelation, Mentions


class Relationship:
    def __init__(self, other_character: Character):
        self.sentiment_value = 0
        self.other_character = other_character

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
        relationship.sentiment_value += sentiment_value
