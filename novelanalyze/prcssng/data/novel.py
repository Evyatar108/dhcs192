from typing import List

from novelanalyze.prcssng.data.char import Character
from novelanalyze.prcssng.data.loc import Location
from novelanalyze.prcssng.data.org import Organization

class NovelEntities:
    def __init__(self, characters: List[Character], locations: List[Location], organizations: List[Organization]):
        self.characters = characters
        self.locations = locations
        self.organizations = organizations
