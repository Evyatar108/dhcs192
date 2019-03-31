import copy

from Analyzation.TextAnalyzation.text_analysis import Relation


class RelationNormalizer:

    def Normalize(self, relationData: Relation):
        copied_relation = copy.copy(relationData)

        if copied_relation.object in ('her', 'his'):
            copied_relation.object += "'s"

        if copied_relation.relation_str == 'is':
            if "'s" in copied_relation.subject and "'s" not in copied_relation.object:  # we should probably not treat the case "'s" is in both
                copied_relation.object, copied_relation.subject = copied_relation.subject, copied_relation.object
                copied_relation.object_span_in_sentence, copied_relation.subject_span_in_sentence = copied_relation.subject_span_in_sentence, copied_relation.object_span_in_sentence

            if "'s" in relationData.object: # todo - update span too
                copied_relation.object, _, relation = relationData.object.partition('\'s')
                copied_relation.relation_str = f'is the {relation} of'

        return copied_relation
