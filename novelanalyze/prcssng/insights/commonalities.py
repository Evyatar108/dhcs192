# coding=utf-8
from itertools import combinations
from typing import List, Generator

from novelanalyze.analyztn.parsedata import Relation
from novelanalyze.prcssng.entitydata import NamedEntity, CommonalityRelation, ExtendedRelation

common_relation_to_relation = {'per_children': 'per_siblings', 'per_other_family': 'per_other_family'}


def __is_convertible_common_relation(common_relation: CommonalityRelation) -> bool:
    return common_relation.relation_str in common_relation_to_relation.keys()


def process(named_entities: List[NamedEntity]) -> None:
    common_relations_to_convert = {}
    for first_entity, second_entity in combinations(named_entities, 2):
        for first_entity_ext_relation in first_entity.get_as_subject_critical_relations():
            for second_entity_ext_relation in second_entity.get_as_subject_critical_relations():
                if __are_same_common_relation(first_entity_ext_relation, second_entity_ext_relation):
                    new_commonality_relation = CommonalityRelation(
                        max(first_entity_ext_relation.indx_chapter, second_entity_ext_relation.indx_chapter),
                        first_entity_ext_relation.relation.relation_str,
                        first_entity, second_entity,
                        first_entity_ext_relation.object_named_entity)
                    first_entity.add_commonality_relation(new_commonality_relation)
                    second_entity.add_commonality_relation(new_commonality_relation)
                    if __is_convertible_common_relation(new_commonality_relation):
                        common_relations_to_convert[
                            __common_relation_as_tuple(new_commonality_relation)] = new_commonality_relation

    for common_relation in common_relations_to_convert.values():
        new_relation_str = common_relation_to_relation[common_relation.relation_str]

        ext_relation = __create_ext_relation(common_relation.indx_chapter, common_relation.first_entity,
                                             common_relation.second_entity, new_relation_str)
        common_relation.first_entity.add_relation_as_subject(ext_relation)
        common_relation.second_entity.add_relation_as_object(ext_relation)

        mirrored_ext_relation = __create_ext_relation(common_relation.indx_chapter, common_relation.second_entity,
                                                      common_relation.first_entity, new_relation_str)
        common_relation.second_entity.add_relation_as_subject(mirrored_ext_relation)
        common_relation.first_entity.add_relation_as_object(mirrored_ext_relation)


def __are_same_common_relation(relation: ExtendedRelation, other_relation: ExtendedRelation) -> bool:
    return relation.relation.relation_str == other_relation.relation.relation_str \
           and relation.object_named_entity == other_relation.object_named_entity


def __common_relation_as_tuple(common_relation: CommonalityRelation):
    return (common_relation.relation_str, common_relation.first_entity,
            common_relation.second_entity, common_relation.common_object_entity)


def __create_ext_relation(indx_chapter: int, subject_entity: NamedEntity, object_entity: NamedEntity,
                          relation_str: str):
    fake_span = (-2, -1)
    relation = Relation(-1, subject_entity.names[0], fake_span, relation_str, fake_span,
                        object_entity.names[0], fake_span)
    ext_relation = ExtendedRelation(relation, subject_entity, object_entity,
                                    indx_chapter)
    return ext_relation