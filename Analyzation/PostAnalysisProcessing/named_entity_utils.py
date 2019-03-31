from typing import Generator, Callable, Tuple, List

from Analyzation.PostAnalysisProcessing.ObjectModels.named_entity_data import NamedEntity


def __ranges_intersect(first_range: Tuple[int, int], second_range: Tuple[int, int]):
    return first_range[0] <= second_range[0] <= first_range[1] \
           or first_range[0] <= second_range[1] <= first_range[1]


def __intersects_entity_reference_span(named_entity: NamedEntity, target_spank: Tuple[int, int],
                                       indx_chapter):
    if indx_chapter not in named_entity.chapters_mentions:
        return False
    return any(__ranges_intersect(target_spank, coref.span_in_sentence)
               for coref in named_entity.chapters_mentions[indx_chapter].coreferences) \
           or any(__ranges_intersect(target_spank, tagged_entity.span_in_sentence)
                  for tagged_entity in named_entity.chapters_mentions[indx_chapter].tagged_entities)


def __find_named_entities_by_span(named_entities, target_spans: Generator[Tuple[int, int]],
                                  indx_chapter: int) -> List[NamedEntity]:
    the_named_entities = [named_entity for named_entity in named_entities if any(
        __intersects_entity_reference_span(named_entity, target_span, indx_chapter) for target_span in
        target_spans)]
    return the_named_entities


def find_named_entities_by_name(named_entities, target_names: Generator[str],
                                pred: Callable[[str, str], bool]) -> List[NamedEntity]:
    the_named_entities = [(named_entity for named_entity in named_entities
                           if any(
        pred(entity_name, target_name) for entity_name in named_entity.names for target_name in target_names))]
    return the_named_entities


def find_named_entities(named_entities, target_spans: Generator[Tuple[int, int]], indx_chapter,
                        target_names: Generator[str],
                        is_same_name_pred: Callable[[str, str], bool]):
    the_named_entities = __find_named_entities_by_span(named_entities, target_spans, indx_chapter)
    if not the_named_entities:
        the_named_entities = find_named_entities_by_name(named_entities, target_names, is_same_name_pred)

    return the_named_entities
