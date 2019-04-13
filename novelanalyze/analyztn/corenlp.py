# coding=utf-8
import copy
import itertools
from typing import Dict, Callable

from stanfordcorenlp import StanfordCoreNLP
import json

from novelanalyze.analyztn.parsedata import *


def analyze(text) -> Tuple[TextAnalysis, Dict]:
    raw_data = __request_data(text)

    #todo - handle "They" as coreference to the last two persons if no coreference was made in the model

    sentences = __extract_sentimented_sentences(raw_data)
    tagged_entities = __extract_tagged_entities(raw_data)
    coreferences_clusters = __extract_coreferences_clusters(raw_data)
    relations = __extract_openie_relations(raw_data)
    return TextAnalysis(sentences, tagged_entities, coreferences_clusters, relations), raw_data


def __request_data(text):
    nlp = StanfordCoreNLP(r'../../stanford-corenlp-full-2018-10-05')
    try:
        data_as_text = nlp.annotate(text, properties={
            'annotators': 'coref, tokenize,ssplit, ner, sentiment, openie, kbp, pos, lemma, parse',
            'outputFormat': 'json',
            'coref.algorithm': 'neural',
            'timeout': '50000'})
    finally:
        nlp.close()
    return json.loads(data_as_text)


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
        if not prev_elem or pred_same_cluster(prev_elem):
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
                         span_in_sentence=(coref['startIndex'] - 1, coref['endIndex'] - 2),
                         is_representative_mention=coref['isRepresentativeMention'])
             for coref in corefs_cluster]
            for corefs_cluster in raw_data['corefs'].values()]


def __extract_openie_relations(raw_data) -> List[Relation]:
    relations = [
        Relation(indx_sentence=sentence_obj['index'], subject_name=raw_relation['subject'],
                 subject_span_in_sentence=tuple(raw_relation['subjectSpan']),
                 relation_str=raw_relation['relation'], relation_span=raw_relation['relationSpan'],
                 object_name=raw_relation['object'], object_span_in_sentence=tuple(raw_relation['objectSpan']))
        for sentence_obj in raw_data['sentences'] for raw_relation in
        itertools.chain(sentence_obj['openie'], sentence_obj['kbp'])]

    normalized_relations = map(normalize_relation, relations)
    return list(normalized_relations)


def normalize_relation(relation_data: Relation):
    copied_relation = copy.copy(relation_data)

    if copied_relation.object_name in ('her', 'his'):
        copied_relation.object_name += "'s"

    if copied_relation.relation_str == 'is':
        if "'s" in copied_relation.subject_name and "'s" not in copied_relation.object_name:
            # we should probably not treat the case "'s" is in both
            copied_relation.object_name, copied_relation.subject_name = \
                copied_relation.subject_name, copied_relation.object_name
            copied_relation.object_span_in_sentence, copied_relation.subject_span_in_sentence = \
                copied_relation.subject_span_in_sentence, copied_relation.object_span_in_sentence

        if "'s" in relation_data.object_name:  # todo - update span too?
            copied_relation.object_name, _, relation = relation_data.object_name.partition('\'s')
            copied_relation.relation_str = f'is the {relation} of'

    return copied_relation


if __name__ == "__main__":
    # # "Israel is a nice place"  # 'Renya walked him to school everyday. She\'d talk to him about love. Then, once they got to the school, Renya would leave him and go do math alone. Ichi couldn\'t fathom what she was thinking, playing around like that. Ichi knew Reyna was lying to him. Ichi could smell it on her.'

    example_sentence = 'Ok go. John is the brother of Joseph'# 'Ron and Anny are father and son'  # 'Zorian’s eyes abruptly shot open as a sharp pain erupted from his stomach. His whole body convulsed, buckling against the object that fell on him, and suddenly he was wide awake, not a trace of drowsiness in his mind. “Good morning, brother!” an annoyingly cheerful voice sounded right on top of him. “Morning, morning, MORNING!!!” Zorian glared at his little sister, but she just smiled back at him cheekily, still sprawled across his stomach. She was humming to herself in obvious satisfaction, kicking her feet playfully in the air as she studied the giant world map Zorian had tacked to the wall next to his bed. Or rather, pretended to study – Zorian could see her watching him intently out of the corner of her eyes for a reaction. This was what he got for not arcane locking the door and setting up a basic alarm perimeter around his bed. “Get off,” he told her in the calmest voice he could muster. “Mom said to wake you up,” she said matter-of-factly, not budging from her spot. “Not like this, she didn’t,” Zorian grumbled, swallowing his irritation and patiently waiting till she dropped her guard. Predictably, Kirielle grew visibly agitated after only a few moments of this pretend disinterest. Just before she could blow up, Zorian quickly grasped her legs and chest and flipped her over the edge of the bed. She fell to the floor with a thud and an indignant yelp, and Zorian quickly jumped to his feet to better respond to any violence she might decide to retaliate with. He glanced down on her and sniffed disdainfully. “I’ll be sure to remember this the next time I’m asked to wake you up.”'
    print('Executing Text Analysis')
    text_analysis, data = analyze(example_sentence)
    print('Finished Text Analysis')
    pass
