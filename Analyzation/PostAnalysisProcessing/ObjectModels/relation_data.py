from Analyzation.PostAnalysisProcessing.ObjectModels.character_data import Character
from Analyzation.PostAnalysisProcessing.ObjectModels.named_entity_data import NamedEntity
from Analyzation.TextAnalyzation.text_analysis import Relation


class ExtendedRelation:
    def __init__(self, relation: Relation, subject_named_entity: NamedEntity, object_named_entity: NamedEntity, indx_chapter: int):
        self.relation = relation
        self.subject_named_entity = subject_named_entity
        self.object_named_entity = object_named_entity


class Relationship:
    def __init__(self, other_character: Character):
        self.sentiment_value = 0
        self.other_character = other_character