# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from novelanalyze.analyztn.parsedata import Relation, CoReference, TaggedTextEntity


@dataclass
class ExtendedRelation:
    relation: Relation
    subject_named_entity: NamedEntity

    def __init__(self, relation: Relation, subject_named_entity: NamedEntity, object_named_entity: NamedEntity,
                 indx_chapter: int):
        self.relation = relation
        self.subject_named_entity = subject_named_entity
        self.object_named_entity = object_named_entity
        self.indx_chapter = indx_chapter


@dataclass
class Mentions:
    indx_chapter: int
    coreferences: List[CoReference] = field(default_factory=list)
    tagged_entities: List[TaggedTextEntity] = field(default_factory=list)


@dataclass
class NamedEntity:
    names: List[str]
    chapters_mentions: Dict[int, Mentions] = field(default_factory=list)
    relations_as_subject: Dict[int, List[ExtendedRelation]] = field(default_factory=dict)
    relations_as_object: Dict[int, List[ExtendedRelation]] = field(default_factory=dict)

    def add_tagged_entity(self, tagged_entity: TaggedTextEntity, indx_chapter: int):
        self.names.append(tagged_entity.text)
        chapter_mentions = self.chapters_mentions.setdefault(indx_chapter, Mentions(indx_chapter))
        chapter_mentions.tagged_entities.append(tagged_entity)

    def add_coreferences_cluster(self, coreferences_cluster: List[CoReference], indx_chapter: int):
        for coreference in coreferences_cluster:
            self.add_coreference(coreference, indx_chapter)

    def add_coreference(self, coreference: CoReference, indx_chapter: int):
        if coreference.ref_type == 'PROPER':
            self.names.append(self.__sanitize_name(coreference.text))
        chapter_mentions = self.chapters_mentions.setdefault(indx_chapter, Mentions(indx_chapter))
        chapter_mentions.coreferences.append(coreference)

    @staticmethod
    def __sanitize_name(name: str):
        return name.strip().partition('\'s')[0]

    def add_relation_as_subject(self, relation: ExtendedRelation, indx_chapter: int):
        chapter_subject_relations = self.relations_as_subject.setdefault(indx_chapter, [])
        chapter_subject_relations.append(relation)

    def add_relation_as_object(self, relation: ExtendedRelation, indx_chapter: int):
        chapter_object_relations = self.relations_as_object.setdefault(indx_chapter, [])
        chapter_object_relations.append(relation)


@dataclass
class Relationship:
    other_character: Character
    sentiment_value: int = 0


@dataclass
class Character(NamedEntity):
    indx_char: int
    gender: str = "UNKNOWN"
    # by chapter and then by char index
    chapters_relationships: Dict[int, Dict[int, Relationship]] = field(default_factory=list)

    def add_relationship_sentiment(self, character, sentiment_value: int, indx_chapter: int):
        chapter_relationships = self.chapters_relationships.setdefault(indx_chapter, {})
        relationship: Relationship = chapter_relationships.setdefault(character.indx, Relationship(character))
        relationship.sentiment_value += sentiment_value


@dataclass
class Location(NamedEntity):
    pass


@dataclass
class Organization(NamedEntity):
    pass


@dataclass
class NovelEntities:
    characters: List[Character] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    organizations: List[Organization] = field(default_factory=list)
