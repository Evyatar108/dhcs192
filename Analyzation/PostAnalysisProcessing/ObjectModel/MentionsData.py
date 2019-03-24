from typing import List

from Analyzation.TextAnalyzation.TextAnalysis import CoReference, TaggedTextEntity


class Mentions:
    def __init__(self, indx_chapter, coreferences: List[CoReference]=[], tagged_entities: List[TaggedTextEntity]=[]):
        self.indx_chapter = indx_chapter
        self.coreferences = coreferences
        self.tagged_entities = tagged_entities