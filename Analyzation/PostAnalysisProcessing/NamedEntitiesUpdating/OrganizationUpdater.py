from typing import List

from Analyzation.PostAnalysisProcessing.ObjectModels.LocationData import Location
from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.NamedEntitiesUpdaterBase import NamedEntityUpdaterBase
from Analyzation.TextAnalyzation.TextAnalysis import TaggedTextEntity, CoReference, TextAnalysis


class OrganizationNamedEntityUpdater(NamedEntityUpdaterBase):

    def update_locations_information(self, text_analysis: TextAnalysis, locations: List[Location], indx_chapter):
        super(OrganizationNamedEntityUpdater, self).update(text_analysis=text_analysis,
                                                           named_entitys=locations,
                                                           indx_chapter=indx_chapter)

    def __is_matched_mention(self, tagged_entity: TaggedTextEntity):
        return any(tagged_entity.tag == location_identifier for location_identifier in
                   ('LOCATION', 'CITY', 'COUNTRY', 'STATE_OR_PROVINCE'))

    def __add_new_named_entitiy_to_list(self, named_entities):
        named_entities.append(Location())

    def __is_matching_coref(self, coreference: CoReference):
        return coreference.animacy == 'INANIMATE' and coreference.type in ('PROPER', 'LIST')