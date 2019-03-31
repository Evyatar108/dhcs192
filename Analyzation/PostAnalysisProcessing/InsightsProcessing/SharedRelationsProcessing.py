
## chars 1,2 got relation 'are' with 'siblings' as the subject and it's the same 'are'
from typing import List

from Analyzation.PostAnalysisProcessing.ObjectModels.CharacterData import Character
from Analyzation.PostAnalysisProcessing.ObjectModels.NamedEntityData import NamedEntity


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