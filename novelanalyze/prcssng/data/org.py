from typing import List, Dict

from novelanalyze.prcssng.data.entity import NamedEntity, ExtendedRelation, Mentions


class Organization(NamedEntity):
    def __init__(self, names: List[str] = [], chapters_mentions: Dict[int, Mentions] = {},
                 relations_as_subject: List[ExtendedRelation] = [], relations_as_object: List[ExtendedRelation] = []):
        super().__init__(names, chapters_mentions, relations_as_subject, relations_as_object)

