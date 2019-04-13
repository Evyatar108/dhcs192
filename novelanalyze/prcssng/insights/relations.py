# coding=utf-8
import re
from typing import List, Iterator

from novelanalyze.prcssng.entitydata import NamedEntity, Character, ExtendedRelation


class RelationRule:
    def __init__(self, regex_rule: str, new_relation: str, subject_type: type(NamedEntity),
                 object_type: type(NamedEntity)):
        self.regex_relation_rule = regex_rule
        self.new_relation = new_relation
        self.subject_type = subject_type
        self.object_type = object_type


relation_rules = [
    RelationRule(regex_rule='is the sibling of|is the brother of|is the sister of|', new_relation='per_siblings',
                 subject_type=Character, object_type=Character)

]


def process(named_entities: Iterator[NamedEntity]):
    for named_entity in named_entities:
        ext_relations = (ext_relation for chapter_ext_relations in named_entity.relations_as_subject.values() for
                         ext_relation in chapter_ext_relations)
        for ext_relation in ext_relations:
            _process_rules_for_relation(ext_relation)


# todo - old relations are overrided with a new relation by the rules, should we do it like this?
def _process_rules_for_relation(ext_relation: ExtendedRelation):
    for relation_rule in relation_rules:
        if _relation_fit_rule(ext_relation, relation_rule):
            ext_relation.relation = relation_rule.new_relation
            return


def _relation_fit_rule(ext_relation: ExtendedRelation, relation_rule: RelationRule):
    return isinstance(ext_relation.subject_named_entity, relation_rule.subject_type) \
           and isinstance(ext_relation.object_named_entity, relation_rule.object_type) \
           and re.search(relation_rule.regex_relation_rule, ext_relation.relation.relation_str)
