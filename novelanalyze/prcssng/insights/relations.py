# coding=utf-8
import re
from dataclasses import dataclass
from typing import Iterator

from novelanalyze.prcssng.entitydata import NamedEntity, Character, ExtendedRelation


@dataclass
class RelationRule:
    regex_rule: str
    new_relation: str
    subject_type: type(NamedEntity)
    object_type: type(NamedEntity)
    new_opposite_relation: str
    switch_roles: bool


relation_rules = [
    RelationRule(regex_rule='is the sibling of|is the brother of|is the sister of', new_relation='per_siblings',
                 subject_type=Character, object_type=Character, new_opposite_relation='per_siblings',
                 switch_roles=False),
    RelationRule(regex_rule='is the mother of|is the mom of| is the father of|is the dad of', new_relation='per_parent',
                 subject_type=Character, object_type=Character, new_opposite_relation='per_children',
                 switch_roles=False),
    RelationRule(regex_rule='is the wife of|is the husband of', new_relation='per_spouse',
                 subject_type=Character, object_type=Character, new_opposite_relation='per_spouse',
                 switch_roles=False),

]


def process(named_entities: Iterator[NamedEntity]) -> None:
    for named_entity in named_entities:
        ext_relations = (ext_relation for chapter_ext_relations in named_entity.relations_as_subject.values() for
                         ext_relation in chapter_ext_relations)
        for ext_relation in ext_relations:
            __process_rules_for_relation(ext_relation)


# todo - old relations are overrided with a new relation by the rules, should we do it like this?
def __process_rules_for_relation(ext_relation: ExtendedRelation) -> None:
    for relation_rule in relation_rules:
        if __relation_fit_rule(ext_relation, relation_rule):
            ext_relation.relation = relation_rule.new_relation
            return


def __relation_fit_rule(ext_relation: ExtendedRelation, relation_rule: RelationRule) -> bool:
    return isinstance(ext_relation.subject_named_entity, relation_rule.subject_type) \
           and isinstance(ext_relation.object_named_entity, relation_rule.object_type) \
           and re.search(relation_rule.regex_relation_rule, ext_relation.relation.relation_str)
