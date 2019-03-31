from typing import List

from Analyzation.PostAnalysisProcessing.ObjectModels.CharacterData import Character
from Analyzation.PostAnalysisProcessing.ObjectModels.LocationData import Location
from Analyzation.PostAnalysisProcessing.ObjectModels.OrganizationData import Organization


class BookData:
    def __init__(self, characters: List[Character], locations: List[Location], organizations: List[Organization]):
        self.characters = characters
        self.locations = locations
        self.organizations = organizations