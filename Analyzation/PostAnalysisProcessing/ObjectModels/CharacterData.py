from typing import Dict, List

from Analyzation.PostAnalysisProcessing.ObjectModels.MentionsData import Mentions
from Analyzation.PostAnalysisProcessing.ObjectModels.NamedEntityData import NamedEntity
from Analyzation.PostAnalysisProcessing.ObjectModels.RelationData import ExtendedRelation


class Character(NamedEntity):
    def __init__(self, indx: int, names: List[str] =[], chapters_mentions: Dict[int, Mentions] = {},
                 relations_as_subject: List[ExtendedRelation]=[], relations_as_object: List[ExtendedRelation]=[],
                 gender="UNKNOWN", chapters_relationships: Dict[int, Dict[int, Relationship]] = {}):
        super().__init__(names, chapters_mentions, relations_as_subject, relations_as_object)
        self.indx = indx
        self.gender = gender
        self.chapters_relationships = chapters_relationships
