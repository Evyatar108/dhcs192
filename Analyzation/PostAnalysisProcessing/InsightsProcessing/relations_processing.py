from typing import List

from Analyzation.PostAnalysisProcessing.ObjectModels.character_data import Character
from Analyzation.PostAnalysisProcessing.ObjectModels.named_entity_data import NamedEntity

class RelationRule:
    def __init__(self, regex_rule, new_relation, subject_type, object_type):
        self.regex_rule = regex_rule
        self.new_relation = new_relation
        self.subject_type = subject_type
        self.object_type = object_type

relation_rules = [
    RelationRule(regex_rule='is the sibling of|is the brother of|is the sister of|', new_relation='per_siblings', subject_type=Character, object_type=Character)

]

def process(named_entities: List[NamedEntity]):
    for named_entity in named_entities:
        #todo
        pass

