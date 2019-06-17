# coding=utf-8
import copy
import itertools
from typing import Dict, Callable
from novelanalyze.analyztn.parsedata import *


def convert_to_local_obj(raw_data: Dict) -> TextAnalysis:
    sentences = __extract_sentimented_sentences(raw_data)
    tagged_entities = __extract_tagged_entities(raw_data)
    coreferences_clusters = __extract_coreferences_clusters(raw_data)
    relations = __extract_openie_relations(raw_data)
    return TextAnalysis(sentences, tagged_entities, coreferences_clusters, relations)


def __extract_sentimented_sentences(raw_data) -> List[SentimentedSentence]:
    sentimented_sentences = []
    for sentence_obj in raw_data['sentences']:
        text = "".join([token['originalText'] + token['after'] for token in sentence_obj['tokens']])
        sentiment = sentence_obj['sentiment']
        sentimented_sentences.append(SentimentedSentence(text=text, sentiment=sentiment,
                                                         sentiment_value=int(sentence_obj['sentimentValue']) - 2))
    return sentimented_sentences


def __extract_tagged_entities(raw_data) -> List[TaggedTextEntity]:
    tagged_tokens = []
    for indx, s in enumerate(raw_data['sentences']):
        for token in s['tokens']:
            tagged_tokens.append(TaggedTextEntity(text=token['originalText'], tag=token['ner'], indx_sentence=indx,
                                                  span_in_sentence=(token['index'] - 1, token['index'] - 1)))
    tagged_entities = __get_continuous_tagged_chunks(tagged_tokens)
    return tagged_entities


def __get_continuous_tagged_chunks(tagged_tokens: List[TaggedTextEntity]) -> List[TaggedTextEntity]:
    tagged_tokens_clusters_gen = __generate_clusters(tagged_tokens, __pred_same_tagged_entity)
    tagged_entities = [TaggedTextEntity(
        text=" ".join([tagged_token.text for tagged_token in tagged_tokens_cluster]),
        tag=tagged_tokens_cluster[0].tag,
        indx_sentence=tagged_tokens_cluster[0].indx_sentence,
        span_in_sentence=(
            tagged_tokens_cluster[0].span_in_sentence[0], tagged_tokens_cluster[-1].span_in_sentence[1]))
        for tagged_tokens_cluster in tagged_tokens_clusters_gen]
    return tagged_entities


def __pred_same_tagged_entity(curr_tagged_token: TaggedTextEntity):
    return curr_tagged_token.tag != 'O'


def __generate_clusters(tagged_tokens: List[TaggedTextEntity], pred_same_cluster: Callable[[TaggedTextEntity], bool]):
    cluster = []
    prev_elem = None
    for elem in tagged_tokens:
        if not prev_elem or pred_same_cluster(elem):
            cluster.append(elem)
        elif cluster:
            yield cluster
            cluster = []
        prev_elem = elem
    if cluster:
        yield cluster


def __extract_coreferences_clusters(raw_data) -> List[List[CoReference]]:
    return [[CoReference(text=coref['text'],
                         ref_type=coref['type'],
                         plurality=coref['number'],
                         gender=coref['gender'],
                         animacy=coref['animacy'],
                         indx_sentence=coref['sentNum'] - 1,
                         span_in_sentence=__fix_span([coref['startIndex'], coref['endIndex']], 1),
                         is_representative_mention=coref['isRepresentativeMention'])
             for coref in corefs_cluster]
            for corefs_cluster in raw_data['corefs'].values()]


def __extract_openie_relations(raw_data) -> List[Relation]:
    relations = [
        Relation(indx_sentence=sentence_obj['index'], subject_name=raw_relation['subject'],
                 subject_span_in_sentence=__fix_span(raw_relation['subjectSpan'], 0),
                 relation_str=raw_relation['relation'], relation_span=__fix_span(raw_relation['relationSpan'], 0),
                 object_name=raw_relation['object'], object_span_in_sentence=__fix_span(raw_relation['objectSpan'], 0))
        for sentence_obj in raw_data['sentences'] for raw_relation in
        itertools.chain(sentence_obj['openie'])]#, sentence_obj['kbp'])]

    normalized_relations = map(normalize_relation, relations)
    return list(normalized_relations)


def __fix_span(span: List[int], offset: int)-> Tuple[int, int]:
    return span[0]-offset, span[1]-offset-1


def normalize_relation(relation_data: Relation):
    copied_relation = copy.copy(relation_data)

    def normalize_word(word):
        if word in ('her', 'his'):
            word += "'s"
        return word

    split_subject_name = [normalize_word(word) for word in copied_relation.subject_name.split(' ')]
    copied_relation.subject_name = ' '.join(split_subject_name)

    split_object_name = [normalize_word(word) for word in copied_relation.object_name.split(' ')]
    copied_relation.object_name = ' '.join(split_object_name)

    if copied_relation.relation_str == 'is' or copied_relation.relation_str == 'was':
        if "'s" in copied_relation.subject_name and "'s" not in copied_relation.object_name:
            # we should probably not treat the case "'s" is in both
            copied_relation.object_name, copied_relation.subject_name = \
                copied_relation.subject_name, copied_relation.object_name
            copied_relation.object_span_in_sentence, copied_relation.subject_span_in_sentence = \
                copied_relation.subject_span_in_sentence, copied_relation.object_span_in_sentence

        if "'s" in relation_data.object_name:  # todo - update span too?
            copied_relation.object_name, _, relation = relation_data.object_name.partition('\'s')
            copied_relation.relation_str += f'{relation} of'

    return copied_relation
