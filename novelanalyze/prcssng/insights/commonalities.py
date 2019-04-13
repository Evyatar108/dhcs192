# coding=utf-8
from itertools import combinations
from typing import List

from novelanalyze.prcssng.entitydata import NamedEntity, CommonalityRelation


def process(named_entities: List[NamedEntity]):
    for first_entity, second_entity in combinations(named_entities, 2):
        for first_entity_ext_relation in __get_as_subject_critical_relations(first_entity):
            for second_entity_ext_relation in __get_as_subject_critical_relations(second_entity):
                if first_entity_ext_relation.relation.relation_str == second_entity_ext_relation.relation.relation_str \
                        and first_entity_ext_relation.object_named_entity == first_entity_ext_relation.object_named_entity:
                    new_commonality_relation = CommonalityRelation(first_entity_ext_relation.relation.relation_str, first_entity, second_entity, first_entity_ext_relation.object_named_entity)
                    first_entity.add_commonality_relation(new_commonality_relation)
                    second_entity.add_commonality_relation(new_commonality_relation)


def __get_as_subject_critical_relations(named_entity: NamedEntity):
    return (ext_relation for ext_relations in named_entity.relations_as_subject.values() for ext_relation in
            ext_relations if '_' in ext_relation.relation.relation_str)
# todo
