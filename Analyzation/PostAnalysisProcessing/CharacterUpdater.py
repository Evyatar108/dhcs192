import itertools
from collections import defaultdict
from typing import List, Callable, Generator, TypeVar, Tuple, Set, Dict

from Analyzation.PostAnalysisProcessing.ObjectModel.CharacterData import Character, Mentions
from Analyzation.PostAnalysisProcessing.ObjectModel.CharactersRelationData import CharactersRelation
from Analyzation.TextAnalyzation.TextAnalysis import TextAnalysis, CoReference, TaggedEntity, Relation, \
    SentimentedSentence


class CharacterUpdater:

    def update_characters_information(self, text_analysis: TextAnalysis, characters: List[Character], indx_chapter):
        self.__process_tagged_entities(text_analysis, characters, indx_chapter)
        self.__process_coreferences(text_analysis, characters, indx_chapter)
        self.__process_relations(text_analysis, characters)
        self.__update_relationships(text_analysis, characters)
        self.__update_genders(characters)

    def __process_tagged_entities(self, text_analysis, characters, indx_chapter):
        tagged_person_entities = (tagged_entity for tagged_entity in text_analysis.tagged_entities if
                                  self.__is_named_person_mention(tagged_entity))
        is_same_char_pred = lambda char_name, tagged_entity_name: char_name in tagged_entity_name.text or tagged_entity_name.text in char_name
        for tagged_person_entity in tagged_person_entities:
            the_character = self.__find_character_by_name(characters, tagged_person_entity.text,
                                                          is_same_char_pred)
            if not the_character:
                the_character = Character(indx=len(characters))
                characters.append(the_character)
            the_character.add_tagged_entity(tagged_person_entity)

    def __is_named_person_mention(self, tagged_entity: TaggedEntity):
        return tagged_entity.tag == 'PERSON'

    def __process_coreferences(self, text_analysis, characters, indx_chapter):
        is_same_char_by_name_pred = lambda char_name, coref_name: char_name in coref_name
        for coreferences_cluster in text_analysis.coreferences_clusters:
            corefs_locs = (coref.span_in_sentence for coref in coreferences_cluster)
            person_coref_name_iter = (coref.text for coref in coreferences_cluster if
                                      self.__is_named_person_coreference(coref))
            the_character = self.__find_character(characters, corefs_locs, person_coref_name_iter,
                                                  is_same_char_by_name_pred)
            if the_character:
                the_character.add_coreferences_cluster(indx_chapter, coreferences_cluster)

    def __is_named_person_coreference(self, coreference: CoReference):
        return coreference.animacy == 'ANIMATE' and coreference.type == 'PROPER'

    def __process_relations(self, text_analysis, characters):
        is_same_char_by_name_pred = lambda char_name,name_in_relation: char_name in name_in_relation or name_in_relation in char_name
        for relation in text_analysis.relations:
            the_subject_character = self.__find_character(characters, relation.subject_span_in_sentence,
                                                          relation.subject,
                                                          is_same_char_by_name_pred)
            the_object_character = self.__find_character(characters, relation.object_span_in_sentence,
                                                         relation.object,
                                                         is_same_char_by_name_pred)
            if the_subject_character is not None:
                if the_object_character is not None:
                    chars_relation = CharactersRelation(relation, the_subject_character, the_object_character)
                    the_subject_character.add_chars_relation_as_subject(chars_relation)
                    the_object_character.add_chars_relation_as_object(chars_relation)
                else:
                    the_subject_character.add_all_relation_as_subject(relation)
            else:
                if the_object_character is not None:
                    the_object_character.add_all_relation_as_object(relation)

    def __find_character(self, characters, target_locs: Generator[Tuple[int, int]], target_names: Generator[str],
                         is_same_name_pred: Callable[[str, str], bool]):
        the_character = self.__find_character_by_loc(characters, target_locs)
        if the_character is None:
            the_character = self.__find_character_by_name(characters, target_names, is_same_name_pred)

        return the_character

    def __find_character_by_loc(self, characters, target_locs: Generator[Tuple[int, int]]) -> Character:
        the_character = next((character for character in characters if any(
            self.__intersects_char_reference_loc(character, target_loc) for target_loc in target_locs)), None)
        return the_character

    def __intersects_char_reference_loc(self, character: Character, target_lock: Tuple[int, int], indx_chapter):
        if indx_chapter not in character.chapters_mentions:
            return False
        return any(self.__ranges_intersect(target_lock, coref.span_in_sentence)
                   for coref in character.chapters_mentions[indx_chapter].coreferences) \
               or any(self.__ranges_intersect(target_lock, tagged_entity.span_in_sentence)
                      for tagged_entity in character.chapters_mentions[indx_chapter].tagged_entities)

    def __ranges_intersect(self, first_range: Tuple[int, int], second_range: Tuple[int, int]):
        return first_range[0] <= second_range[0] <= first_range[1] \
               or first_range[0] <= second_range[1] <= first_range[1]

    def __find_character_by_name(self, characters, target_names: Generator[str],
                                 pred: Callable[[str, str], bool]) -> Character:
        the_character = next((character for character in characters
                              if any(
            pred(char_name, target_name) for char_name in character.names for target_name in target_names)), None)
        return the_character


    def __update_relationships(self, characters: List[Character], sentences: List[SentimentedSentence], indx_chapter: int):
        mentioned_characters_in_sentences: List[Set[Character]] = [{}] * len(sentences)
        for character in characters:
            for mentions in character.chapters_mentions[indx_chapter]:
                for tagged_entity in mentions.tagged_entities:
                    mentioned_characters_in_sentences[tagged_entity.indx_sentence].add(character)

        mentioned_characters_in_sentences: List[List[Character]] = [list(set_of_characters) for set_of_characters in mentioned_characters_in_sentences]

        for characters_in_sentence, sentence in zip(mentioned_characters_in_sentences, sentences):
            for indx_first_character, first_character in enumerate(characters_in_sentence):
                for second_character in characters_in_sentence[indx_first_character+1:]:
                    first_character.add_relationship_sentiment(second_character, sentence.sentiment_value)
                    second_character.add_relationship_sentiment(first_character, sentence.sentiment_value)

    def __update_genders(self, characters):
        genders_count: Dict[str, int] = defaultdict(int)
        for character in characters:
            for coref in (coref for mentions in itertools.chain(character.chapters_mentions.values()) for coref in
                          mentions.coreferences):
                genders_count[coref.gender] += 1
            character.gender = max(genders_count, genders_count.get)
