# coding=utf-8
import copy
import re
from typing import List

from novelanalyze.analyztn.parsedata import Relation
from novelanalyze.prcssng.entitydata import NamedEntity, Character, ExtendedRelation
from novelanalyze.prcssng.utils import find_named_entities, find_as_subject_relation


class SharedRelationRule:
    def __init__(self, entity_type, object_regex_rule: str, new_relation: str):
        self.entity_type = entity_type
        self.object_regex_rule = object_regex_rule
        self.new_relation = new_relation


shared_relation_rules: List[SharedRelationRule] = [
    SharedRelationRule(Character, 'siblings|brothers|sisters', 'per_sibling')
]


def process(named_entities: List[NamedEntity]):
    for named_entity in named_entities:
        for chapter_relations in named_entity.relations_as_subject.values():
            for ext_relation in chapter_relations:
                _process_rules_for_relation(named_entities, ext_relation)


def _process_rules_for_relation(named_entities: List[NamedEntity], ext_relation: ExtendedRelation):
    if ext_relation.relation.relation_str == 'are':
        for relation_rule in shared_relation_rules:
            if _relation_fit_rule(ext_relation, relation_rule):
                subject_named_entities = find_named_entities(ext_relation.indx_chapter, named_entities,
                                                             [ext_relation.relation.subject_span_in_sentence])
                for second_entity in subject_named_entities:
                    _update_named_entities_with_shared_relation(ext_relation, relation_rule, second_entity)
                pass
                return


def _relation_fit_rule(ext_relation: ExtendedRelation, relation_rule: SharedRelationRule):
    return isinstance(ext_relation.subject_named_entity, relation_rule.entity_type) \
           and re.search(relation_rule.object_regex_rule, ext_relation.relation.relation_str)


def _update_named_entities_with_shared_relation(ext_relation: ExtendedRelation, relation_rule: SharedRelationRule,
                                                second_entity: NamedEntity):
    first_entity = ext_relation.subject_named_entity
    indx_chapter = ext_relation.indx_chapter
    # we dont want to add this relation twice, so we ensure we do it only for one ordered pair of named entities
    if hash(first_entity) < hash(second_entity):
        connected_relation = find_as_subject_relation(indx_chapter, second_entity,
                                                      ext_relation.relation.object_span_in_sentence)
        new_relation = Relation(indx_chapter,
                                ext_relation.relation.subject_name, ext_relation.relation.subject_span_in_sentence,
                                relation_rule.new_relation, (-2, -1),
                                connected_relation.relation.subject_name,
                                connected_relation.relation.subject_span_in_sentence)
        mirrored_new_relation = copy.copy(new_relation)

        mirrored_new_relation.subject_name = new_relation.object_name
        mirrored_new_relation.subject_span_in_sentence = new_relation.subject_span_in_sentence
        mirrored_new_relation.object_name = new_relation.subject_name
        mirrored_new_relation.object_span_in_sentence = new_relation.subject_span_in_sentence

        new_ext_relation = ExtendedRelation(new_relation, first_entity, second_entity, indx_chapter)
        mirrored_new_ext_relation = ExtendedRelation(new_relation, second_entity, first_entity, indx_chapter)

        first_entity.add_relation_as_subject(new_ext_relation, indx_chapter)
        second_entity.add_relation_as_object(new_ext_relation, indx_chapter)

        first_entity.add_relation_as_object(mirrored_new_ext_relation, indx_chapter)
        second_entity.add_relation_as_subject(mirrored_new_ext_relation, indx_chapter)