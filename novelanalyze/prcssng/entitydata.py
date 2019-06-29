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

    def create_opposite(self, opp_relation_str=None):
        opp_relation_str = self.relation.relation_str if opp_relation_str is None else opp_relation_str
        opp_relation = Relation(self.indx_chapter, self.relation.object_name, self.relation.object_span_in_sentence,
                                opp_relation_str, self.relation.relation_span, self.relation.subject_name,
                                self.relation.subject_span_in_sentence)
        opp_ext_relation = ExtendedRelation(opp_relation, self.object_named_entity, self.subject_named_entity,
                                            self.indx_chapter)

        return opp_ext_relation


@dataclass
class CommonalityRelation:
    indx_chapter: int
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

    def __init__(self, names: List[str] = None):
        self.names = names if names is not None else []
        self.coref_names = []
        self.name = names[0] if names is not None else None
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
        self.coref_names.append(coreference.text)
        chapter_mentions = self.chapters_mentions.setdefault(indx_chapter, Mentions(indx_chapter))
        chapter_mentions.coreferences.append(coreference)

    def add_relation_as_subject(self, relation: ExtendedRelation):
        chapter_subject_relations = self.relations_as_subject.setdefault(relation.indx_chapter, [])
        chapter_subject_relations.append(relation)

    def add_relation_as_object(self, relation: ExtendedRelation):
        chapter_object_relations = self.relations_as_object.setdefault(relation.indx_chapter, [])
        chapter_object_relations.append(relation)

    def add_commonality_relation(self, relation: CommonalityRelation):
        self.commonalities_relations.append(relation)

    def __hash__(self):
        return id(self)

    def get_as_subject_kbp_relations(self) -> Iterator[ExtendedRelation]:
        return self.__gen_each_relation_once(
            (ext_relation for ext_relation in chain.from_iterable(self.relations_as_subject.values()) if
             self.__is_kbp_relation(ext_relation)))

    def get_as_object_kbp_relations(self) -> Iterator[ExtendedRelation]:
        return self.__gen_each_relation_once(
            (ext_relation for ext_relation in chain.from_iterable(self.relations_as_object.values()) if
             self.__is_kbp_relation(ext_relation)))

    def get_kbp_relations(self) -> Iterator[ExtendedRelation]:
        return self.__gen_each_relation_once(
            chain(self.get_as_subject_kbp_relations(), self.get_as_object_kbp_relations()))

    def get_coreferences(self) -> Iterator[CoReference]:
        return (coref for chapter_mentions in self.chapters_mentions.values() for coref in
                chapter_mentions.coreferences)

    @staticmethod
    def __gen_each_relation_once(relations: Iterator[ExtendedRelation]):
        seen_relations = set()
        for ext_relation in relations:
            relation_as_tuple = (ext_relation.relation.relation_str, ext_relation.object_named_entity)
            if relation_as_tuple not in seen_relations:
                seen_relations.add(relation_as_tuple)
                yield ext_relation

    @staticmethod
    def __is_kbp_relation(ext_relation: ExtendedRelation):
        return True  # ':' in ext_relation.relation.relation_str todo


@dataclass
class Relationship:
    other_character: Character
    sentiment_value: int = 0


class Character(NamedEntity):
    def __init__(self, names: List[str] = None):
        super(Character, self).__init__(names)
        self.gender: str = "UNKNOWN"
        self.chapters_relationships: Dict[int, Dict[Character, Relationship]] = {}

    def add_relationship_sentiment(self, character: Character, sentiment_value: int, indx_chapter: int):
        chapter_relationships = self.chapters_relationships.setdefault(indx_chapter, {})
        relationship: Relationship = chapter_relationships.setdefault(character, Relationship(character))
        relationship.sentiment_value += sentiment_value


class Location(NamedEntity):
    def __init__(self, names: List[str] = None):
        super(Location, self).__init__(names)


class Organization(NamedEntity):
    def __init__(self, names: List[str] = None):
        super(Organization, self).__init__(names)


@dataclass
class NovelEntities:
    name: str
    characters: List[Character] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    organizations: List[Organization] = field(default_factory=list)

    def get_named_entities(self) -> Iterator[NamedEntity]:
        return chain(self.characters, self.locations, self.organizations)
