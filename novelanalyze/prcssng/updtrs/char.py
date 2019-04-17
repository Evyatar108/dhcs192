# coding=utf-8
import itertools
from collections import Counter
from typing import List, Set
from novelanalyze.prcssng.entitydata import Character, NamedEntity
from novelanalyze.prcssng.updtrs.base import NamedEntityUpdaterBase
from novelanalyze.analyztn.parsedata import TextAnalysis, CoReference, TaggedTextEntity, SentimentedSentence


class CharacterNamedEntityUpdater(NamedEntityUpdaterBase):

    def update_characters_information(self, text_analysis: TextAnalysis, characters: List[Character],
                                      indx_chapter: int) -> None:
        super(CharacterNamedEntityUpdater, self).update(text_analysis=text_analysis,
                                                        named_entitys=characters,
                                                        indx_chapter=indx_chapter)
        self.__update_relationships(characters, text_analysis.sentimented_sentences, indx_chapter)
        self.__update_genders(characters)

    def __is_matched_mention(self, tagged_entity: TaggedTextEntity) -> bool:
        return tagged_entity.tag == 'PERSON'

    def __add_new_named_entitiy_to_list(self, named_entities: List[NamedEntity]) -> None:
        named_entities.append(Character())

    def __is_matching_coref(self, coreference: CoReference) -> bool:
        return coreference.animacy == 'ANIMATE' and coreference.ref_type in ('PROPER', 'LIST')

    @staticmethod
    def __update_relationships(characters: List[Character], sentences: List[SentimentedSentence],
                               indx_chapter: int) -> None:
        mentioned_characters_in_sentences: List[Set[Character]] = [{}] * len(sentences)
        for character in characters:
            mentions = character.chapters_mentions[indx_chapter]
            for tagged_entity in mentions.tagged_entities:
                mentioned_characters_in_sentences[tagged_entity.indx_sentence].add(character)

        mentioned_characters_in_sentences: List[List[Character]] = [list(set_of_characters) for set_of_characters in
                                                                    mentioned_characters_in_sentences]

        for characters_in_sentence, sentence in zip(mentioned_characters_in_sentences, sentences):
            for first_character, second_character in itertools.combinations(characters_in_sentence, 2):
                first_character.add_relationship_sentiment(second_character, sentence.sentiment_value, indx_chapter)
                second_character.add_relationship_sentiment(first_character, sentence.sentiment_value, indx_chapter)

    @staticmethod
    def __update_genders(characters: List[Character]) -> None:
        for character in characters:
            corefs = (coref for mentions in itertools.chain(character.chapters_mentions.values()) for coref in
                      mentions.coreferences)
            character.gender, _ = Counter(corefs).most_common(1)[0]
