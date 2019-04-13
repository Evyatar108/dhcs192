# coding=utf-8
from abc import abstractmethod
from typing import List
from novelanalyze.analyztn.parsedata import TextAnalysis, CoReference, TaggedTextEntity
from novelanalyze.prcssng import utils
from novelanalyze.prcssng.entitydata import NamedEntity, ExtendedRelation
from novelanalyze.prcssng.utils import find_named_entity


class NamedEntityUpdaterBase:
    def __init__(self):
        raise Exception("Unimplemented class")

    def update(self, text_analysis: TextAnalysis, named_entitys: List[NamedEntity],
               indx_chapter):
        self.__process_tagged_entities(text_analysis, named_entitys, indx_chapter)
        self.__process_coreferences(text_analysis, named_entitys, indx_chapter)
        self.__process_relations(text_analysis, named_entitys, indx_chapter)

    def __process_tagged_entities(self, text_analysis, named_entities, indx_chapter) -> None:
        matching_tagged_entities = (tagged_entity for tagged_entity in text_analysis.tagged_entities if
                                    self.__is_matched_mention(tagged_entity))

        def is_same_named_entity_pred(named_entity_name, tagged_entity_name):
            return named_entity_name in tagged_entity_name.text or tagged_entity_name.text in named_entity_name

        for matching_tagged_entity in matching_tagged_entities:
            the_named_entity: NamedEntity = find_named_entity(named_entities, [], indx_chapter,
                                                              matching_tagged_entity.text,
                                                              is_same_named_entity_pred)
            if the_named_entity is None:
                self.__add_new_named_entitiy_to_list(named_entities)
                the_named_entity.add_tagged_entity(matching_tagged_entity, indx_chapter)

    @abstractmethod
    def __is_matched_mention(self, tagged_entity: TaggedTextEntity) -> bool:
        pass

    @abstractmethod
    def __add_new_named_entitiy_to_list(self, named_entities) -> None:
        pass

    def __process_coreferences(self, text_analysis, named_entities, indx_chapter) -> None:
        def is_same_named_entity_pred(named_entity_name, coref_name):
            return named_entity_name in coref_name

        for coreferences_cluster in text_analysis.coreferences_clusters:
            corefs_spans = (coref.span_in_sentence for coref in coreferences_cluster)
            matching_coref_name_iter = (coref.text for coref in coreferences_cluster if
                                        self.__is_matching_coref(coref))
            the_named_entities = utils.find_named_entities(indx_chapter, named_entities, corefs_spans,
                                                           matching_coref_name_iter,
                                                           is_same_named_entity_pred)
            for the_named_entity in the_named_entities:
                the_named_entity.add_coreferences_cluster(indx_chapter, coreferences_cluster)

    def __is_matching_coref(self, coreference: CoReference) -> bool:
        raise Exception("Unimplemented")

    @staticmethod
    def __process_relations(text_analysis, named_entities, indx_chapter) -> None:
        def is_same_named_entity_pred(named_entity_name, name_in_relation):
            return named_entity_name in name_in_relation or name_in_relation in named_entity_name

        for relation in text_analysis.relations:
            the_subject_named_entity = utils.find_named_entity(named_entities, relation.subject_span_in_sentence,
                                                               indx_chapter,
                                                               relation.subject,
                                                               is_same_named_entity_pred)
            the_object_named_entity = utils.find_named_entity(named_entities, relation.object_span_in_sentence,
                                                              indx_chapter,
                                                              relation.object,
                                                              is_same_named_entity_pred)

            extended_relation = ExtendedRelation(relation, the_subject_named_entity, the_object_named_entity,
                                                 indx_chapter)

            if the_subject_named_entity is not None:
                the_subject_named_entity.add_relation_as_subject(extended_relation, indx_chapter)
            if the_object_named_entity is not None:
                the_object_named_entity.add_relation_as_subject(extended_relation, indx_chapter)
