from typing import List

from novelanalyze.prcssng.data.char import Character
from novelanalyze.prcssng.data.entity import NamedEntity


class SharedRelationRule:
    def __init__(self, entity_type ,object_regex_rule, new_relation):
        self.entity_type = entity_type
        self.object_regex_rule = object_regex_rule
        self.new_relation = new_relation

shared_relation_rules: List[SharedRelationRule] = [
    SharedRelationRule(Character ,'siblings|brothers|sisters', 'per_sibling')
]

def process(named_entities: List[NamedEntity]):
    for named_entity in named_entities:
        for relation in named_entity.relations_as_subject:
            if relation.relation_str == 'are':
                #todo
                pass
    pass
