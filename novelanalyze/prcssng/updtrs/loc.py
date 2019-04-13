# coding=utf-8
from typing import List

from novelanalyze.prcssng.entitydata import Location, NamedEntity
from novelanalyze.prcssng.updtrs.base import NamedEntityUpdaterBase
from novelanalyze.analyztn.parsedata import TaggedTextEntity, CoReference, TextAnalysis


class LocationNamedEntityUpdater(NamedEntityUpdaterBase):

    def update_locations_information(self, text_analysis: TextAnalysis, locations: List[Location], indx_chapter: int):
        super(LocationNamedEntityUpdater, self).update(text_analysis=text_analysis,
                                                       named_entitys=locations,
                                                       indx_chapter=indx_chapter)

    def __is_matched_mention(self, tagged_entity: TaggedTextEntity):
        return any(tagged_entity.tag == location_identifier for location_identifier in
                   ('LOCATION', 'CITY', 'COUNTRY', 'STATE_OR_PROVINCE'))

    def __add_new_named_entitiy_to_list(self, named_entities: List[NamedEntity]):
        named_entities.append(Location())

    def __is_matching_coref(self, coreference: CoReference):
        return coreference.animacy == 'INANIMATE' and coreference.ref_type in ('PROPER', 'LIST')
