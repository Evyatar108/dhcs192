from typing import Generator, Callable, Tuple

from Analyzation.PostAnalysisProcessing.ObjectModels.NamedEntityData import NamedEntity


def find_named_entity(named_entities, target_spans: Generator[Tuple[int, int]], indx_chapter,
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


def find_named_entity_by_name(self, named_entities, target_names: Generator[str],
                                pred: Callable[[str, str], bool]) -> NamedEntity:
    the_named_entity = next((named_entity for named_entity in named_entities
                             if any(
        pred(entity_name, target_name) for entity_name in named_entity.names for target_name in target_names)),
                            None)
    return the_named_entity
