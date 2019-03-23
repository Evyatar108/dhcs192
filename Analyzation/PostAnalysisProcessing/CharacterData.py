from typing import List

from Analyzation.PostAnalysisProcessing.RelationsData import Relation
from Analyzation.TextAnalyzation.TextAnalysis import CoReference, TaggedEntity


# consists of both names entities and coreferences of the same character
class Mentions:
    def __init__(self, indx_chapter, coreferences: List[CoReference], tagged_entities: List[TaggedEntity] ):
        self.indx_chapter = indx_chapter
        self.coreferences =  coreferences
        self.tagged_entities = tagged_entities

class Character:
    def __init__(self, gender, names: List[str], chapters_mentions: List[Mentions], relations:List[Relation]):
        self.gender = gender
        self.names = names
        self.chapters_mentions = chapters_mentions
        self.relations = relations

    def add_tagged_entity(self, indx_chapter, tagged_entity: TaggedEntity):
        self.names.append(tagged_entity.text)
        self.__try_add_chapter_mentions(indx_chapter)
        self.chapters_mentions[indx_chapter-1].tagged_entities.append(tagged_entity)

    def add_coreferences_cluster(self, indx_chapter, coreferences_cluster: List[CoReference]):
        for coreference in coreferences_cluster:
            self.add_coreference(indx_chapter, coreference)

    def add_coreference(self, indx_chapter, coreference: CoReference):
        if (coreference.type == 'PROPER'):
            self.names.append(self.__sanitize_name(coreference.text))
        self.__try_add_chapter_mentions(indx_chapter)
        self.chapters_mentions[indx_chapter-1].coreferences.append(coreference)

    def __sanitize_name(self, name: str):
        return name.strip().partition('\'s')[0]


    def __try_add_chapter_mentions(self, indx_chapter):
        if len(self.chapters_mentions) < indx_chapter:
            self.chapters_mentions.append(Mentions(indx_chapter, [], []))
