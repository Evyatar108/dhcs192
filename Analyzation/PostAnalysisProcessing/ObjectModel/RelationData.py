from Analyzation.PostAnalysisProcessing.ObjectModel.NamedEntityData import NamedEntity
from Analyzation.TextAnalyzation.TextAnalysis import Relation


class ExtendedRelation:
    def __init__(self, relation: Relation, subject_named_entity: NamedEntity, object_named_entity: NamedEntityBase):
        self.relation = relation
        self.subject_named_entity = subject_named_entity
        self.object_named_entity = object_named_entity
