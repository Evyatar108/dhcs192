# coding=utf-8
from typing import Callable, Tuple, List, Iterator

from novelanalyze.prcssng.entitydata import NamedEntity, ExtendedRelation


def find_as_subject_relation(indx_chapter: int, named_entity: NamedEntity,
                             relation_span: Tuple[int, int]) -> ExtendedRelation:
    return next((relation for relation in named_entity.relations_as_subject[indx_chapter] if
                 relation.relation.relation_span == relation_span), None)


def find_named_entity(indx_chapter: int, indx_sentence: int, named_entities: List[NamedEntity],
                      target_spans: List[Tuple[int, int]] = iter([]),
                      target_names: List[str] = iter([]),
                      is_same_name_pred: Callable[[str, str], bool] = None) -> NamedEntity:
    the_named_entities = find_named_entities(indx_chapter, indx_sentence, named_entities, target_spans, target_names,
                                             is_same_name_pred)
    x = next(iter(the_named_entities), None)
    return x


def find_named_entities(indx_chapter: int, indx_sentence: int, named_entities: List[NamedEntity],
                        target_spans: List[Tuple[int, int]] = iter(()),
                        target_names: List[str] = iter(()),
                        is_same_name_pred: Callable[[str, str], bool] = None) -> List[NamedEntity]:
    the_named_entities = list(__find_named_entities_by_span(named_entities, target_spans, indx_chapter, indx_sentence))
    if the_named_entities:
        return the_named_entities
    return list(__find_named_entities_by_name(named_entities, target_names, is_same_name_pred))


def __find_named_entities_by_name(named_entities: List[NamedEntity], target_names: List[str],
                                  pred: Callable[[str, str], bool]) -> Iterator[NamedEntity]:
    return (named_entity for named_entity in named_entities if
            any(pred(target_name, entity_name) for target_name in target_names for entity_name in named_entity.names))


def __find_named_entities_by_span(named_entities, target_spans: List[Tuple[int, int]],
                                  indx_chapter: int, indx_sentence: int) -> Iterator[NamedEntity]:
    the_named_entities = [named_entity for named_entity in named_entities if any(
        __intersects_entity_reference_span(named_entity, target_span, indx_chapter, indx_sentence) for target_span in
        target_spans)]
    return iter(the_named_entities)


def __intersects_entity_reference_span(named_entity: NamedEntity, target_span: Tuple[int, int],
                                       indx_chapter: int, indx_sentence: int) -> bool:
    if indx_chapter not in named_entity.chapters_mentions:
        return False
    return any(__ranges_intersect(target_span, coref.span_in_sentence) and coref.indx_sentence == indx_sentence
               for coref in named_entity.chapters_mentions[indx_chapter].coreferences) or any(
        __ranges_intersect(target_span, tagged_entity.span_in_sentence) and tagged_entity.indx_sentence == indx_sentence
        for tagged_entity in named_entity.chapters_mentions[indx_chapter].tagged_entities)


def __ranges_intersect(first_range: Tuple[int, int], second_range: Tuple[int, int]) -> bool:
    return first_range[0] <= second_range[0] <= first_range[1] \
           or first_range[0] <= second_range[1] <= first_range[1]
