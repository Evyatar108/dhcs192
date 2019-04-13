# coding=utf-8
import re
from itertools import combinations
from typing import List, Iterator

from novelanalyze.analyztn.parsedata import Relation
from novelanalyze.prcssng.entitydata import NamedEntity, Character, ExtendedRelation
from novelanalyze.prcssng.utils import find_named_entities


class SharedRelationRule:
    def __init__(self, entity_type, object_regex_rule: str, new_relation: str):
        self.entity_type = entity_type
        self.object_regex_rule = object_regex_rule
        self.new_relation = new_relation
        self.related_pairs = {}


shared_relation_rules: List[SharedRelationRule] = [
    SharedRelationRule(Character, 'siblings|brothers|sisters', 'per_sibling')
]


def process(named_entities: List[NamedEntity]):
    for named_entity in named_entities:
        for chapter_relations in named_entity.relations_as_subject.values():
            for ext_relation in chapter_relations:
                _process_rules_for_relation(ext_relation)


def _process_rules_for_relation(ext_relation: ExtendedRelation):
    if ext_relation.relation.relation_str == 'are':
        for relation_rule in shared_relation_rules:
            if relation_fit_rule(ext_relation, relation_rule):
                if
                    subject_named_entities = find_named_entities(ext_relation.indx_chapter, named_entities,
                                                                 ext_relation.relation.subject_span_in_sentence)
                for first_entity, second_entity in combinations(subject_named_entities, 2):
                    new_relation = Relation(ext_relation.indx_chapter, ext_relation.relation.subject_name,
                                            ext_relation.relation.subject_span_in_sentence, )
                # todo
                pass
                return


def _relation_fit_rule(ext_relation: ExtendedRelation, relation_rule: SharedRelationRule):
    return isinstance(ext_relation.subject_named_entity, relation_rule.subject_type) \
           and isinstance(ext_relation.object_named_entity, relation_rule.object_type) \
           and re.search(relation_rule.regex_rule, ext_relation.relation.relation_str)