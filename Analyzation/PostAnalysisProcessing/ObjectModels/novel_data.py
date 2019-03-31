from typing import List

from Analyzation.PostAnalysisProcessing.ObjectModels.character_data import Character
from Analyzation.PostAnalysisProcessing.ObjectModels.location_data import Location
from Analyzation.PostAnalysisProcessing.ObjectModels.OrganizationData import Organization

class NovelEntities:
    def __init__(self, characters: List[Character], locations: List[Location], organizations: List[Organization]):
        self.characters = characters
        self.locations = locations
        self.organizations = organizations
