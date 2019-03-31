from typing import Dict, List
from __future__ import annotations

from novelanalyze.analyztn.data import TaggedTextEntity, CoReference, Relation


class ExtendedRelation:
    def __init__(self, relation: Relation, subject_named_entity: NamedEntity, object_named_entity: NamedEntity, indx_chapter: int):
        self.relation = relation
        self.subject_named_entity = subject_named_entity
        self.object_named_entity = object_named_entity
        self.indx_chapter = indx_chapter

class Mentions:
    def __init__(self, indx_chapter, coreferences: List[CoReference]=[], tagged_entities: List[TaggedTextEntity]=[]):
        self.indx_chapter = indx_chapter
        self.coreferences = coreferences
        self.tagged_entities = tagged_entities

class NamedEntity:
    def __init__(self, names: List[str], chapters_mentions: Dict[int, Mentions],
                 relations_as_subject: Dict[int, List[ExtendedRelation]], relations_as_object: Dict[int, List[ExtendedRelation]]):
        self.names = names
        self.chapters_mentions = chapters_mentions

        self.relations_as_subject = relations_as_subject
        self.relations_as_object = relations_as_object

    def add_tagged_entity(self, tagged_entity: TaggedTextEntity, indx_chapter: int):
        self.names.add(tagged_entity.text)
        chapter_mentions = self.chapters_mentions.setdefault(indx_chapter, [])
        chapter_mentions.tagged_entities.append(tagged_entity)

    def add_coreferences_cluster(self, indx_chapter, coreferences_cluster: List[CoReference]):
        for coreference in coreferences_cluster:
            self.add_coreference(indx_chapter, coreference)

    def add_coreference(self, coreference: CoReference, indx_chapter,):
        if (coreference.type == 'PROPER'):
            self.names.add(self.__sanitize_name(coreference.text))
        chapter_mentions = self.chapters_mentions.setdefault(indx_chapter, [])
        chapter_mentions.coreferences.append(coreference)

    def __sanitize_name(self, name: str):
        return name.strip().partition('\'s')[0]

    def add_relation_as_subject(self, relation: ExtendedRelation, indx_chapter: int):
        chapter_subject_relations = self.relations_as_subject.setdefault(indx_chapter,[])
        chapter_subject_relations.append(relation)

    def add_relation_as_object(self, relation: ExtendedRelation, indx_chapter: int):
        chapter_object_relations = self.relations_as_object.setdefault(indx_chapter, [])
        chapter_object_relations.append(relation)