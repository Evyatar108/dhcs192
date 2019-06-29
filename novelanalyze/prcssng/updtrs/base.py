# coding=utf-8
from abc import abstractmethod, ABCMeta
from collections import Counter
from itertools import chain, combinations
from typing import List, Tuple

from novelanalyze.analyztn.parsedata import TextAnalysis, CoReference, TaggedTextEntity
from novelanalyze.prcssng import utils
from novelanalyze.prcssng.entitydata import NamedEntity, ExtendedRelation
from novelanalyze.prcssng.utils import find_named_entity


class NamedEntityUpdaterBase(object):
    __metaclass__ = ABCMeta
    speaker_indx = 1

    def update(self, text_analysis: TextAnalysis, named_entities: List[NamedEntity],
               indx_chapter):
        print('Creating named entities based on tagged entities')
        self.__process_tagged_entities(text_analysis, named_entities, indx_chapter)
        print('Merging named entited')
        self.__merge_named_entities(named_entities)
        print('Matching coreferences to named entities')
        self.__process_coreferences(text_analysis, named_entities, indx_chapter)
        print('Matching relations to named entities')
        self.__process_relations(text_analysis, named_entities, indx_chapter)
        print('Updating display name of named entities')
        self.__update_most_common_name(named_entities)

    def __process_tagged_entities(self, text_analysis: TextAnalysis, named_entities: List[NamedEntity],
                                  indx_chapter: int) -> None:
        matching_tagged_entities = (tagged_entity for tagged_entity in text_analysis.tagged_entities if
                                    self._is_matched_mention(tagged_entity))

        def is_same_named_entity_pred(named_entity_name, tagged_entity_name):
            return named_entity_name in tagged_entity_name or tagged_entity_name in named_entity_name

        for matching_tagged_entity in matching_tagged_entities:
            the_named_entity: NamedEntity = find_named_entity(indx_chapter, matching_tagged_entity.indx_sentence,
                                                              named_entities, [],
                                                              [matching_tagged_entity.text],
                                                              is_same_named_entity_pred)
            if the_named_entity is None:
                the_named_entity = self._add_new_named_entitiy_to_list(named_entities)
            the_named_entity.add_tagged_entity(matching_tagged_entity, indx_chapter)

    # todo - move merging to a common place to avoid duplication of logic which is used in the speaker file too
    def __merge_named_entities(self, named_entities: List[NamedEntity]):
        found_merge = True
        while found_merge:
            found_merge = False
            entity, other_entity = self.__find_compatible_merge(named_entities)
            if entity is not None and other_entity is not None:
                found_merge = True
                for chapter_indx in other_entity.chapters_mentions.keys():
                    for coref in other_entity.chapters_mentions[chapter_indx].coreferences:
                        entity.add_coreference(coref, chapter_indx)
                    for tagged_entity in other_entity.chapters_mentions[chapter_indx].tagged_entities:
                        entity.add_tagged_entity(tagged_entity, chapter_indx)
                named_entities.remove(other_entity)
                for named_entity in named_entities:
                    for ext_relation in chain.from_iterable(named_entity.relations_as_subject.values()):
                        if ext_relation.object_named_entity == other_entity:
                            ext_relation.object_named_entity = entity
                            entity.add_relation_as_object(ext_relation)
                    for ext_relation in chain.from_iterable(named_entity.relations_as_object.values()):
                        if ext_relation.subject_named_entity == other_entity:
                            ext_relation.subject_named_entity = entity
                            entity.add_relation_as_subject(ext_relation)

    @staticmethod
    def __find_compatible_merge(named_entities: List[NamedEntity]) -> Tuple[NamedEntity, NamedEntity]:
        compatible_merges = (pair for pair in combinations(named_entities, 2) if
                             any(name == other_name for name in pair[0].names for other_name in pair[1].names))
        return next(compatible_merges, (None, None))

    @abstractmethod
    def _is_matched_mention(self, tagged_entity: TaggedTextEntity) -> bool:
        pass

    @abstractmethod
    def _add_new_named_entitiy_to_list(self, named_entities) -> NamedEntity:
        pass

    def __process_coreferences(self, text_analysis, named_entities, indx_chapter) -> None:
        def is_same_named_entity_pred(named_entity_name, coref_name):
            return coref_name in named_entity_name

        for coreferences_cluster in text_analysis.coreferences_clusters:
            the_named_entities = list(
                chain.from_iterable(utils.find_named_entities(indx_chapter, coref.indx_sentence,
                                                              named_entities, [],
                                                              [coref.text],
                                                              is_same_named_entity_pred)
                                    for coref in coreferences_cluster
                                    if self._is_matching_coref(coref)))
            for the_named_entity in the_named_entities:
                the_named_entity.add_coreferences_cluster(coreferences_cluster, indx_chapter)
            if not the_named_entities and coreferences_cluster[0].text.lower() in ['i', 'my']:
                the_named_entity = self._add_new_named_entitiy_to_list(named_entities)
                the_named_entity.add_coreferences_cluster(coreferences_cluster, indx_chapter)
                the_named_entity.names.append(f'Speaker {self.speaker_indx}')
                self.speaker_indx += 1

    @abstractmethod
    def _is_matching_coref(self, coreference: CoReference) -> bool:
        pass

    @staticmethod
    def __process_relations(text_analysis, named_entities, indx_chapter) -> None:
        for relation in text_analysis.relations:
            the_subject_named_entity = utils.find_named_entity_strict(indx_chapter, relation.indx_sentence,
                                                                      named_entities,
                                                                      relation.subject_span_in_sentence,
                                                                      relation.subject_name)
            the_object_named_entity = utils.find_named_entity_strict(indx_chapter, relation.indx_sentence,
                                                                     named_entities,
                                                                     relation.object_span_in_sentence,
                                                                     relation.object_name)

            if the_subject_named_entity is not None and the_object_named_entity is not None:
                extended_relation = ExtendedRelation(relation, the_subject_named_entity, the_object_named_entity,
                                                     indx_chapter)
                the_subject_named_entity.add_relation_as_subject(extended_relation)
                the_object_named_entity.add_relation_as_object(extended_relation)

    def __update_most_common_name(self, named_entities: List[NamedEntity]):
        for named_entity in named_entities:
            most_common_name = Counter(named_entity.names).most_common(1)
            named_entity.name, _ = most_common_name[0]
