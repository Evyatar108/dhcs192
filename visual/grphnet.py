# coding=utf-8
from itertools import chain
from typing import Tuple

from pyvis.network import Network

from novelanalyze.analyztn.parsedata import Relation
from novelanalyze.prcssng.entitydata import NovelEntities, Location, Character, ExtendedRelation


def convert_novel_entities_to_graph(novel_entities: NovelEntities) -> Network:
    graph = Network(directed=True, bgcolor="#222222", font_color="white")
    graph.barnes_hut()
    graph.set_edge_smooth('dynamic')
    for named_entity in novel_entities.get_named_entities():
        value = sum(1 for _ in named_entity.get_critical_relations())
        graph.add_node(id(named_entity), named_entity.names[0], title=named_entity.names[0], value=value)

    for named_entity in novel_entities.get_named_entities():
        for ext_relation in named_entity.get_critical_relations():
                relation_desc, relation_color = __get_relation_name_and_color(ext_relation.relation.relation_str)
                print(relation_desc)
                graph.add_edge(id(ext_relation.subject_named_entity), id(ext_relation.object_named_entity), arrowStrikethrough=True,
                               physics=True, title=relation_desc, color=relation_color)
    return graph


def to_viewable_graph(graph: Network):
    graph.show("mygraph.html")


relations_info = {'per_siblings': 'dodgerblue', 'per_parents': 'lightsteelblue', 'per_other_family': 'deepskyblue', 'per_spouse': 'blueviolet'}


def __get_relation_name_and_color(relation_str: str) -> Tuple[str, str]:
    # todo search in info
    # todo avoid duplicate relations
    # todo add mirrored relations
    return relation_str, 'dodgerblue'


if __name__ == "__main__":
    def create_relation(named_one, named_two, novel_entities):
        mock_span = (-1, -1)
        sibling_relation = Relation(1, named_one.names[0], mock_span, 'per_sibling', mock_span, named_two.names[0],
                                    mock_span)
        ext_sibling_relation = ExtendedRelation(sibling_relation, named_one, named_two, 1)

        brother_relation = Relation(1, named_one.names[0], mock_span, 'per_brother', mock_span, named_two.names[0],
                                    mock_span)
        ext_brother_relation = ExtendedRelation(brother_relation, named_one, named_two, 1)

        named_one.add_relation_as_subject(ext_sibling_relation, 1)
        named_two.add_relation_as_object(ext_sibling_relation, 1)
        named_one.add_relation_as_subject(ext_brother_relation, 1)
        named_two.add_relation_as_object(ext_brother_relation, 1)


    novel_entities = NovelEntities()
    moshe = Character(['Moshe'])
    simba = Character(['Simba'])
    goku = Character(['Goku'])
    create_relation(moshe, simba, novel_entities)
    create_relation(simba, goku, novel_entities)
    create_relation(goku, moshe, novel_entities)
    novel_entities.characters.extend([moshe, simba, goku])

    graph = convert_novel_entities_to_graph(novel_entities)
    to_viewable_graph(graph)
    pass



