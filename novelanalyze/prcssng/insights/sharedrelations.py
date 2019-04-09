# coding=utf-8
from typing import List

from novelanalyze.prcssng.entitydata import NamedEntity, Character


class SharedRelationRule:
    def __init__(self, entity_type, object_regex_rule, new_relation):
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
                if ext_relation.relation.relation_str == 'are':
                    # todo
                    pass
