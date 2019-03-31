from typing import List, Dict

from Analyzation.PostAnalysisProcessing.ObjectModels.MentionsData import Mentions
from Analyzation.PostAnalysisProcessing.ObjectModels.NamedEntityData import NamedEntity
from Analyzation.PostAnalysisProcessing.ObjectModels.RelationData import ExtendedRelation


class Location(NamedEntity):
    def __init__(self, names: List[str] = [], chapters_mentions: Dict[int, Mentions] = {},
                 relations_as_subject: List[ExtendedRelation] = [], relations_as_object: List[ExtendedRelation] = []):
        super().__init__(names, chapters_mentions, relations_as_subject, relations_as_object)

