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


def wrap_words_as_regex_rule(*args: str) -> str:
    return '|'.join(f'is (\w*(-?)){word} of' for word in args)


relation_rules = [
    RelationRule(
        regex_rule=wrap_words_as_regex_rule('sibling', 'brother', 'sister', 'bro', 'sis'), new_relation='per:siblings',
        subject_type=Character, object_type=Character, new_opposite_relation='per:siblings'),
    RelationRule(
        regex_rule=wrap_words_as_regex_rule('mother', 'mom', 'father', 'dad'), new_relation='per:children',
        subject_type=Character, object_type=Character, new_opposite_relation='per:parents'),
    RelationRule(
        regex_rule=wrap_words_as_regex_rule('son', 'daughter', 'child', 'firstborn', 'offspring'),
        new_relation='per:parents', subject_type=Character, object_type=Character,
        new_opposite_relation='per:children'),
    RelationRule(
        regex_rule=wrap_words_as_regex_rule('wife', 'husband', 'spouse', 'bride', 'groom'), new_relation='per:spouse',
        subject_type=Character, object_type=Character, new_opposite_relation='per:spouse'),
    RelationRule(
        regex_rule=wrap_words_as_regex_rule('niece', 'cousin', 'uncle', 'aunt', 'ancestor', 'descendant', 'grandfather',
                                            'grandmother', 'granddaughter', 'grandson'),
        new_relation='per:other_family', subject_type=Character, object_type=Character,
        new_opposite_relation='per:other_family')
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
            ext_relation.relation.relation_str = relation_rule.new_relation
            opposite_relation = ext_relation.create_opposite(relation_rule.new_opposite_relation)

            ext_relation.subject_named_entity.add_relation_as_object(opposite_relation)
            ext_relation.object_named_entity.add_relation_as_subject(opposite_relation)
            return


def __relation_fit_rule(ext_relation: ExtendedRelation, relation_rule: RelationRule) -> bool:
    return isinstance(ext_relation.subject_named_entity, relation_rule.subject_type) \
           and isinstance(ext_relation.object_named_entity, relation_rule.object_type) \
           and re.search(relation_rule.regex_rule, ext_relation.relation.relation_str)
