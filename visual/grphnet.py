# coding=utf-8
from typing import Tuple

from pyvis.network import Network

from novelanalyze.analyztn.parsedata import Relation
from novelanalyze.prcssng.entitydata import NovelEntities, Character, ExtendedRelation


def show_relations_network_graph(novel_entities: NovelEntities) -> None:
    graph = Network(directed=True, bgcolor="#222222", font_color="white")
    graph.barnes_hut()
    graph.set_edge_smooth('dynamic')
    nodes_dict = {}
    for named_entity in novel_entities.get_named_entities():
        nodes_dict[id(named_entity)] = named_entity
        value = sum(1 for _ in named_entity.get_as_subject_kbp_relations())
        title = named_entity.name
        if isinstance(named_entity, Character) and named_entity.gender != "UNKNOWN":
            title += '<br>' + "Gender" + ': ' + named_entity.gender.capitalize()
        for ext_relation in named_entity.get_as_subject_kbp_relations():
            relation_desc, _ = __get_relation_name_and_color(ext_relation.relation.relation_str)
            title += '<br>' + relation_desc.capitalize() + ': ' + ext_relation.object_named_entity.name
        graph.add_node(n_id=id(named_entity), label=named_entity.name, value=value, title=title)

    for named_entity in novel_entities.get_named_entities():
        for ext_relation in named_entity.get_as_subject_kbp_relations():
            relation_desc, relation_color = __get_relation_name_and_color(ext_relation.relation.relation_str)
            # relation_desc += " of"
            print(relation_desc)
            graph.add_edge(id(ext_relation.object_named_entity), id(ext_relation.subject_named_entity),
                           arrowStrikethrough=True,
                           physics=True, title=relation_desc, color=relation_color)

    graph.show(novel_entities.name + '.html')


relations_info = {'per:siblings': ('sibling', 'dodgerblue'),
                  'per:parents': ('parent', 'lightsteelblue'),
                  'per:other_family': ('relative', 'deepskyblue'),
                  'per:spouse': ('spouse', 'blueviolet'),
                  'per:children': ('children', 'lightsalmon')}


def __get_relation_name_and_color(relation_str: str) -> Tuple[str, str]:
    if relation_str not in relations_info:
        return relation_str, 'yellow'
    return relations_info[relation_str]


if __name__ == "__main__":
    def create_relation(named_one, named_two):
        mock_span = (-1, -1)
        sibling_relation = Relation(1, named_one.name, mock_span, 'per:siblings', mock_span, named_two.name,
                                    mock_span)
        ext_sibling_relation = ExtendedRelation(sibling_relation, named_one, named_two, 1)

        other_relation = Relation(1, named_one.name, mock_span, 'per:other_family', mock_span, named_two.name,
                                  mock_span)
        ext_other_relation = ExtendedRelation(other_relation, named_one, named_two, 1)

        named_one.add_relation_as_subject(ext_sibling_relation)
        named_two.add_relation_as_object(ext_sibling_relation)
        named_one.add_relation_as_subject(ext_other_relation)
        named_two.add_relation_as_object(ext_other_relation)


    novel_entities = NovelEntities('example novel')
    moshe = Character(['Moshe'])
    simba = Character(['Simba'])
    goku = Character(['Goku'])
    create_relation(moshe, simba)
    create_relation(simba, goku)
    create_relation(goku, moshe)
    novel_entities.characters.extend([moshe, simba, goku])

    show_relations_network_graph(novel_entities)
    pass
