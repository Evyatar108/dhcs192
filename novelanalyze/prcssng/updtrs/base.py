# coding=utf-8
from abc import abstractmethod, ABCMeta
from collections import Counter
from itertools import chain
from typing import List

from novelanalyze.analyztn.parsedata import TextAnalysis, CoReference, TaggedTextEntity
from novelanalyze.prcssng import utils
from novelanalyze.prcssng.entitydata import NamedEntity, ExtendedRelation
from novelanalyze.prcssng.utils import find_named_entity


class NamedEntityUpdaterBase(object):
    __metaclass__ = ABCMeta

    def update(self, text_analysis: TextAnalysis, named_entities: List[NamedEntity],
               indx_chapter):
        self.__process_tagged_entities(text_analysis, named_entities, indx_chapter)
        self.__process_coreferences(text_analysis, named_entities, indx_chapter)
        self.__process_relations(text_analysis, named_entities, indx_chapter)
        self.__update_most_common_name(named_entities)

    def __process_tagged_entities(self, text_analysis, named_entities, indx_chapter) -> None:
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

    @abstractmethod
    def _is_matched_mention(self, tagged_entity: TaggedTextEntity) -> bool:
        pass

    @abstractmethod
    def _add_new_named_entitiy_to_list(self, named_entities) -> NamedEntity:
        pass

    def __process_coreferences(self, text_analysis, named_entities, indx_chapter) -> None:
        def is_same_named_entity_pred(named_entity_name, coref_name):
            return named_entity_name in coref_name

        for coreferences_cluster in text_analysis.coreferences_clusters:
            the_named_entities = list(
                chain.from_iterable(utils.find_named_entities(indx_chapter, coref.indx_sentence,
                                                              named_entities, [coref.span_in_sentence],
                                                              [coref.text] if self._is_matching_coref(coref) else [],
                                                              is_same_named_entity_pred)
                                    for coref in coreferences_cluster))
            for the_named_entity in the_named_entities:
                the_named_entity.add_coreferences_cluster(coreferences_cluster, indx_chapter)

    @abstractmethod
    def _is_matching_coref(self, coreference: CoReference) -> bool:
        pass

    @staticmethod
    def __process_relations(text_analysis, named_entities, indx_chapter) -> None:
        def is_same_named_entity_pred(named_entity_name, name_in_relation):
            return named_entity_name in name_in_relation or name_in_relation in named_entity_name

        for relation in text_analysis.relations:
            the_subject_named_entity = utils.find_named_entity(indx_chapter, relation.indx_sentence, named_entities,
                                                               [relation.subject_span_in_sentence],
                                                               [relation.subject_name],
                                                               is_same_named_entity_pred)
            the_object_named_entity = utils.find_named_entity(indx_chapter, relation.indx_sentence, named_entities,
                                                              [relation.object_span_in_sentence],
                                                              [relation.object_name],
                                                              is_same_named_entity_pred)

            if the_subject_named_entity is not None and the_object_named_entity is not None:
                extended_relation = ExtendedRelation(relation, the_subject_named_entity, the_object_named_entity,
                                                     indx_chapter)
                the_subject_named_entity.add_relation_as_subject(extended_relation)
                the_object_named_entity.add_relation_as_object(extended_relation)

    def __update_most_common_name(self, named_entities: List[NamedEntity]):
        for named_entity in named_entities:
            most_common_name = Counter(named_entity.names).most_common(1)
            named_entity.name, _ = most_common_name[0]
