from typing import List

from Analyzation.PostAnalysisProcessing.CharacterData import Character, Mentions
from Analyzation.TextAnalyzation.TextAnalysis import TextAnalysis, CoReference, TaggedEntity


class CharacterUpdater:

    def update_characters_information(self, text_analysis: TextAnalysis, characters: List[Character], indx_chapter):
        tagged_person_entities = [tagged_entity for tagged_entity in text_analysis.tagged_entities if
                                  tagged_entity.tag == 'PERSON']

        for tagged_person_entity in tagged_person_entities:
            the_character = self.__find_character(characters, tagged_person_entities=[tagged_person_entity])
            if not the_character:
                the_character = Character(gender='UNKNOWN', names=[tagged_person_entity.text],
                                          mentions=Mentions(indx_chapter, [], [tagged_person_entity]), relations=[])
                characters.append(the_character)

        for coreferences_cluster in text_analysis.coreferences_clusters:
            the_character = self.__find_character(characters, coreferences_cluster)

            if the_character:
                the_character.add_coreferences_cluster(indx_chapter, coreferences_cluster)

    def __find_character(self, characters, coreferences_cluster: List[CoReference] = [],
                         tagged_entities: List[TaggedEntity] = []) -> Character:
        the_character = next((character for character in characters
                              if self.__match_names(character, coreferences_cluster, tagged_entities)))

        return the_character

    def __match_names(self, character: Character, person_coreferences: List[CoReference],
                      tagged_entities: List[TaggedEntity]) -> bool:
        for name in character.names:
            for coreference in person_coreferences:
                if self.__is_named_person_coreference(coreference) and name in coreference.text:
                    return True
            for tagged_entity in tagged_entities:
                if self.__is_named_person_mention(tagged_entity.tag) and (
                        name in tagged_entity.text or tagged_entity.text in name):
                    return True
        return False

    def __is_named_person_coreference(self, coreference: CoReference):
        return coreference.animacy == 'ANIMATE' and coreference.type == 'PROPER'

    def __is_named_person_mention(self, tagged_entity: TaggedEntity):
        return tagged_entity.tag == 'PERSON'
