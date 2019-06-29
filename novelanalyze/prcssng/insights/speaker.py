from itertools import chain
from typing import List

from novelanalyze.prcssng.entitydata import NamedEntity, Character


def process(named_entities: List[NamedEntity]) -> None:
    speakers = [named_entity for named_entity in named_entities if
                isinstance(named_entity, Character) and named_entity.name.startswith('Speaker')]
    __merge_by_relation(speakers, named_entities)
    __merge_storyteller(speakers, named_entities)


def __merge_storyteller(speakers: List[NamedEntity], named_entities: List[NamedEntity]):
    storytellers = [speaker for speaker in speakers if
                    any(coref for coref in speaker.get_coreferences() if coref.speaker == 'PER0')]
    if storytellers:
        storyteller = storytellers[0]
        for other_storyteller in storytellers[1:]:
            __merge(storyteller, other_storyteller, named_entities)


def __merge_by_relation(speakers: List[NamedEntity], named_entities: List[NamedEntity]):
    for speaker in speakers:
        connecting_relation = next(
            (ext_relation for ext_relation in chain.from_iterable(speaker.relations_as_subject.values()) if
             ext_relation.relation.relation_str.lower() in ['is name of', 'am']),
            None)
        if connecting_relation:
            __merge(connecting_relation.object_named_entity, speaker, named_entities)


def __merge(entity: NamedEntity, deleted_entity: NamedEntity, named_entities: List[NamedEntity]):
    for chapter_indx in deleted_entity.chapters_mentions.keys():
        entity.add_coreferences_cluster(deleted_entity.chapters_mentions[chapter_indx].coreferences, chapter_indx)
    for named_entity in named_entities:
        for ex_relation in chain.from_iterable(named_entity.relations_as_subject.values()):
            if ex_relation.object_named_entity == deleted_entity:
                ex_relation.object_named_entity = entity
                entity.add_relation_as_object(ex_relation)
        for ex_relation in chain.from_iterable(named_entity.relations_as_object.values()):
            if ex_relation.subject_named_entity == deleted_entity:
                ex_relation.subject_named_entity = entity
                entity.add_relation_as_subject(ex_relation)
    named_entities.remove(deleted_entity)
