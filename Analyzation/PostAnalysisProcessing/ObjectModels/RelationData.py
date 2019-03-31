from Analyzation.PostAnalysisProcessing.ObjectModels.NamedEntityData import NamedEntity
from Analyzation.TextAnalyzation.TextAnalysis import RelationData


class ExtendedRelation:
    def __init__(self, relation: RelationData, subject_named_entity: NamedEntity, object_named_entity: NamedEntity, indx_chapter: int):
        self.relation = relation
        self.subject_named_entity = subject_named_entity
        self.object_named_entity = object_named_entity
