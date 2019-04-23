# coding=utf-8
from typing import List

from novelanalyze.prcssng.entitydata import NamedEntity, Organization
from novelanalyze.prcssng.updtrs.base import NamedEntityUpdaterBase
from novelanalyze.analyztn.parsedata import TaggedTextEntity, CoReference, TextAnalysis


class OrganizationNamedEntityUpdater(NamedEntityUpdaterBase):

    def update(self, text_analysis: TextAnalysis, organizations: List[Organization],
               indx_chapter: int) -> None:
        super(OrganizationNamedEntityUpdater, self).update(text_analysis=text_analysis,
                                                           named_entities=organizations,
                                                           indx_chapter=indx_chapter)

    def _is_matched_mention(self, tagged_entity: TaggedTextEntity) -> bool:
        return any(tagged_entity.tag == location_identifier for location_identifier in
                   ('LOCATION', 'CITY', 'COUNTRY', 'STATE_OR_PROVINCE'))

    def _add_new_named_entitiy_to_list(self, named_entities: List[NamedEntity]) -> NamedEntity:
        organization = Organization()
        named_entities.append(organization)
        return organization

    def _is_matching_coref(self, coreference: CoReference) -> bool:
        return coreference.animacy == 'INANIMATE' and coreference.ref_type in ('PROPER', 'LIST')
