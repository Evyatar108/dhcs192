# coding=utf-8
from typing import List

from novelanalyze.prcssng.entitydata import Location, NamedEntity
from novelanalyze.prcssng.updtrs.base import NamedEntityUpdaterBase
from novelanalyze.analyztn.parsedata import TaggedTextEntity, CoReference, TextAnalysis


class LocationNamedEntityUpdater(NamedEntityUpdaterBase):

    def update(self, text_analysis: TextAnalysis, locations: List[Location],
               indx_chapter: int) -> None:
        super(LocationNamedEntityUpdater, self).update(text_analysis=text_analysis,
                                                       named_entities=locations,
                                                       indx_chapter=indx_chapter)

    def _is_matched_mention(self, tagged_entity: TaggedTextEntity) -> bool:
        return any(tagged_entity.tag == location_identifier for location_identifier in
                   ('LOCATION', 'CITY', 'COUNTRY', 'STATE_OR_PROVINCE'))

    def _add_new_named_entitiy_to_list(self, named_entities: List[NamedEntity]) -> Location:
        location = Location()
        named_entities.append(location)
        return location

    def _is_matching_coref(self, coreference: CoReference) -> bool:
        return coreference.animacy == 'INANIMATE' and coreference.ref_type in ('PROPER', 'LIST')
