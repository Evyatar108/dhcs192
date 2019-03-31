import itertools
from collections import Counter
from typing import List, Set

from Analyzation.PostAnalysisProcessing.ObjectModels.CharacterData import Character
from Analyzation.PostAnalysisProcessing.NamedEntitiesUpdating.NamedEntitiesUpdaterBase import NamedEntityUpdaterBase
from Analyzation.TextAnalyzation.TextAnalysis import TextAnalysis, CoReference, TaggedTextEntity, SentimentedSentence


class CharacterNamedEntityUpdater(NamedEntityUpdaterBase):

    def update_characters_information(self, text_analysis: TextAnalysis, characters: List[Character], indx_chapter):
        super(CharacterNamedEntityUpdater, self).update(text_analysis=text_analysis,
                                                        named_entitys=characters,
                                                        indx_chapter=indx_chapter)
        self.__update_relationships(text_analysis, characters, indx_chapter)
        self.__update_genders(characters)

    def __is_matched_mention(self, tagged_entity: TaggedTextEntity):
        return tagged_entity.tag == 'PERSON'

    def __add_new_named_entitiy_to_list(self, named_entities):
        named_entities.append(Character(indx=len(named_entities)))

    def __is_matching_coref(self, coreference: CoReference):
        return coreference.animacy == 'ANIMATE' and coreference.type in ('PROPER', 'LIST')

    def __update_relationships(self, characters: List[Character], sentences: List[SentimentedSentence],
                               indx_chapter: int):
        mentioned_characters_in_sentences: List[Set[Character]] = [{}] * len(sentences)
        for character in characters:
            for mentions in character.chapters_mentions[indx_chapter]:
                for tagged_entity in mentions.tagged_entities:
                    mentioned_characters_in_sentences[tagged_entity.indx_sentence].add(character)

        mentioned_characters_in_sentences: List[List[Character]] = [list(set_of_characters) for set_of_characters in
                                                                    mentioned_characters_in_sentences]

        for characters_in_sentence, sentence in zip(mentioned_characters_in_sentences, sentences):
            for indx_first_character, first_character in enumerate(characters_in_sentence):
                for second_character in characters_in_sentence[indx_first_character + 1:]:
                    first_character.add_relationship_sentiment(second_character, sentence.sentiment_value, indx_chapter)
                    second_character.add_relationship_sentiment(first_character, sentence.sentiment_value, indx_chapter)

    def __update_genders(self, characters):
        for character in characters:
            corefs = (coref for mentions in itertools.chain(character.chapters_mentions.values()) for coref in
                      mentions.coreferences)
            character.gender, _ = Counter(corefs).most_common(1)[0]
