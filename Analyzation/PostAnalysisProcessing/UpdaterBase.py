from typing import List, Callable, Generator, Tuple, Set, Dict

from Analyzation.PostAnalysisProcessing.ObjectModel.NamedEntityData import NamedEntity
from Analyzation.PostAnalysisProcessing.ObjectModel.RelationData import ExtendedRelation
from Analyzation.TextAnalyzation.TextAnalysis import TextAnalysis, CoReference, TaggedTextEntity, SentimentedSentence


class UpdaterBase:

    def update_named_entitys_information(self, text_analysis: TextAnalysis, named_entitys: List[NamedEntity],
                                         indx_chapter):
        self.__process_tagged_entities(text_analysis, named_entitys, indx_chapter)
        self.__process_coreferences(text_analysis, named_entitys, indx_chapter)
        self.__process_relations(text_analysis, named_entitys, indx_chapter)

    def __process_tagged_entities(self, text_analysis, named_entities, indx_chapter):
        matching_tagged_entities = (tagged_entity for tagged_entity in text_analysis.tagged_entities if
                                    self.__is_matched_mention(tagged_entity))
        is_same_named_entity_pred = lambda named_entity_name,tagged_entity_name: named_entity_name in tagged_entity_name.text or tagged_entity_name.text in named_entity_name
        for matching_tagged_entity in matching_tagged_entities:
            the_named_entity = self.__find_named_entity_by_name(named_entities, matching_tagged_entity.text,
                                                                is_same_named_entity_pred)
            if the_named_entity is None:
                self.__add_new_named_entitiy_to_list(named_entities)
                the_named_entity.add_tagged_entity(matching_tagged_entity, indx_chapter)

    def __is_matched_mention(self, tagged_entity: TaggedTextEntity):
        raise Exception("Unimplemented")

    def __add_new_named_entitiy_to_list(self, named_entities):
        raise Exception("Unimplemented")

    def __process_coreferences(self, text_analysis, named_entities, indx_chapter):
        is_same_named_entity_pred = lambda named_entity_name, coref_name: named_entity_name in coref_name
        for coreferences_cluster in text_analysis.coreferences_clusters:
            corefs_spans = (coref.span_in_sentence for coref in coreferences_cluster)
            matching_coref_name_iter = (coref.text for coref in coreferences_cluster if
                                        self.__is_matching_coref(coref))
            the_named_entity = self.__find_named_entity(named_entities, corefs_spans, indx_chapter,
                                                        matching_coref_name_iter,
                                                        is_same_named_entity_pred)
            if the_named_entity is not None:
                the_named_entity.add_coreferences_cluster(indx_chapter, coreferences_cluster)

    def __is_matching_coref(self, coreference: CoReference):
        raise Exception("Unimplemented")

    def __process_relations(self, text_analysis, named_entities, indx_chapter):
        is_same_named_entity_pred = lambda named_entity_name,name_in_relation: named_entity_name in name_in_relation or name_in_relation in named_entity_name
        for relation in text_analysis.relations:
            the_subject_named_entity = self.__find_named_entity(named_entities, relation.subject_span_in_sentence,
                                                                indx_chapter,
                                                                relation.subject,
                                                                is_same_named_entity_pred)
            the_object_named_entity = self.__find_named_entity(named_entities, relation.object_span_in_sentence,
                                                               indx_chapter,
                                                               relation.object,
                                                               is_same_named_entity_pred)

            extended_relation = ExtendedRelation(relation, the_subject_named_entity, the_object_named_entity)

            if the_subject_named_entity is not None:
                the_subject_named_entity.add_relation_as_subject(extended_relation, indx_chapter)
            if the_object_named_entity is not None:
                the_object_named_entity.add_relation_as_subject(extended_relation, indx_chapter)

    def __find_named_entity(self, named_entities, target_spans: Generator[Tuple[int, int]], indx_chapter,
                            target_names: Generator[str],
                            is_same_name_pred: Callable[[str, str], bool]):
        the_named_entity = self.__find_named_entity_by_span(named_entities, target_spans, indx_chapter)
        if the_named_entity is None:
            the_named_entity = self.__find_named_entity_by_name(named_entities, target_names, is_same_name_pred)

        return the_named_entity

    def __find_named_entity_by_span(self, named_entities, target_spans: Generator[Tuple[int, int]],
                                    indx_chapter: int) -> NamedEntity:
        the_named_entity = next((named_entity for named_entity in named_entities if any(
            self.__intersects_entity_reference_span(named_entity, target_span, indx_chapter) for target_span in
            target_spans)), None)
        return the_named_entity

    def __intersects_entity_reference_span(self, named_entity: NamedEntity, target_spank: Tuple[int, int],
                                           indx_chapter):
        if indx_chapter not in named_entity.chapters_mentions:
            return False
        return any(self.__ranges_intersect(target_spank, coref.span_in_sentence)
                   for coref in named_entity.chapters_mentions[indx_chapter].coreferences) \
               or any(self.__ranges_intersect(target_spank, tagged_entity.span_in_sentence)
                      for tagged_entity in named_entity.chapters_mentions[indx_chapter].tagged_entities)

    def __ranges_intersect(self, first_range: Tuple[int, int], second_range: Tuple[int, int]):
        return first_range[0] <= second_range[0] <= first_range[1] \
               or first_range[0] <= second_range[1] <= first_range[1]

    def __find_named_entity_by_name(self, named_entities, target_names: Generator[str],
                                    pred: Callable[[str, str], bool]) -> NamedEntity:
        the_named_entity = next((named_entity for named_entity in named_entities
                                 if any(
            pred(entity_name, target_name) for entity_name in named_entity.names for target_name in target_names)),
                                None)
        return the_named_entity
