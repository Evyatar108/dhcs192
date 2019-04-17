# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from typing import Dict, List, Iterator

from novelanalyze.analyztn.parsedata import Relation, CoReference, TaggedTextEntity


@dataclass
class ExtendedRelation:
    relation: Relation
    subject_named_entity: NamedEntity
    object_named_entity: NamedEntity
    indx_chapter: int


@dataclass
class CommonalityRelation:
    relation_str: str
    first_entity: NamedEntity
    second_entity: NamedEntity
    common_object_entity: NamedEntity


@dataclass
class Mentions:
    indx_chapter: int
    coreferences: List[CoReference] = field(default_factory=list)
    tagged_entities: List[TaggedTextEntity] = field(default_factory=list)


class NamedEntity:
    # lists here are first ordered by chapter index using dictionary holding lists for each chapter

    def __init__(self, names: List[str]):
        self.names = names
        self.chapters_mentions: Dict[int, Mentions] = {}
        self.relations_as_subject: Dict[int, List[ExtendedRelation]] = {}
        self.relations_as_object: Dict[int, List[ExtendedRelation]] = {}
        self.commonalities_relations: List[CommonalityRelation] = []

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

    def add_commonality_relation(self, relation: CommonalityRelation):
        self.commonalities_relations.append(relation)

    def __hash__(self):
        return id(self)

    def get_as_subject_critical_relations(self) -> Iterator[ExtendedRelation]:
        return (ext_relation for ext_relation in chain.from_iterable(self.relations_as_subject.values()) if
                self.__is_critical_relation(ext_relation))

    def get_as_object_critical_relations(self) -> Iterator[ExtendedRelation]:
        return (ext_relation for ext_relation in chain.from_iterable(self.relations_as_object.values()) if
                self.__is_critical_relation(ext_relation))

    def get_critical_relations(self) -> Iterator[ExtendedRelation]:
        return chain(self.get_as_subject_critical_relations(), self.get_as_object_critical_relations())

    @staticmethod
    def __is_critical_relation(ext_relation: ExtendedRelation):
        return '_' in ext_relation.relation.relation_str


@dataclass
class Relationship:
    other_character: Character
    sentiment_value: int = 0


class Character(NamedEntity):
    def __init__(self, names: List[str]):
        super(Character, self).__init__(names)
        self.gender: str = "UNKNOWN"
        self.chapters_relationships: Dict[int, Dict[Character, Relationship]] = field(default_factory=list)

    def add_relationship_sentiment(self, character: Character, sentiment_value: int, indx_chapter: int):
        chapter_relationships = self.chapters_relationships.setdefault(indx_chapter, {})
        relationship: Relationship = chapter_relationships.setdefault(character, Relationship(character))
        relationship.sentiment_value += sentiment_value


class Location(NamedEntity):
    def __init__(self, names: List[str]):
        super(Location, self).__init__(names)


class Organization(NamedEntity):
    def __init__(self, names: List[str]):
        super(Organization, self).__init__(names)


@dataclass
class NovelEntities:
    name: str
    characters: List[Character] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    organizations: List[Organization] = field(default_factory=list)

    def get_named_entities(self) -> Iterator[NamedEntity]:
        return chain(self.characters, self.locations, self.organizations)
