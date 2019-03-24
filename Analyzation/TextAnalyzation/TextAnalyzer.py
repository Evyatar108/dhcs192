from typing import Dict

from stanfordcorenlp import StanfordCoreNLP
import json

from Analyzation.TextAnalyzation.TextAnalysis import *


class TextAnalyzer:

    def __init__(self):
        self.nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05')

    def dispose(self):
        self.nlp.close()

    def analyze_text(self, text) -> Tuple[TextAnalysis, Dict]:
        data = self.__request_data(text)
        sentences = self.__extract_sentimented_sentences(data)
        tagged_entities = self.__extract_tagged_entities(data)
        coreferences_clusters = self.__extract_coreferences_clusters(data)
        relations = self.__extract_openie_relations(data)
        return (TextAnalysis(sentences, tagged_entities, coreferences_clusters, relations), data)

    def __request_data(self, text):
        data_as_text = self.nlp.annotate(text, properties={'annotators': 'coref, ssplit, ner, sentiment, openie',
                                                           'outputFormat': 'json'})
        return json.loads(data_as_text)

    def __extract_sentimented_sentences(self, data) -> List[SentimentedSentence]:
        sentimented_sentences = []
        for sentence_obj in data['sentences']:
            text = "".join([token['originalText'] + token['after'] for token in sentence_obj['tokens']])
            sentiment = sentence_obj['sentiment']
            sentimented_sentences.append(SentimentedSentence(text=text, sentiment=sentiment, sentiment_value=(-1) * (
                    int(sentence_obj['sentimentValue']) - 2)))
        return sentimented_sentences

    def __extract_tagged_entities(self, data) -> List[TaggedEntity]:
        tagged_tokens = []
        for indx, s in enumerate(data['sentences']):
            for token in s['tokens']:
                tagged_tokens.append(TaggedEntity(text=token['originalText'], tag=token['ner'], indx_sentence=indx,
                                                  span_in_sentence=(token['index'] - 1, token['index'] - 1)))
        tagged_entities = self.__get_continuous_tagged_chunks(tagged_tokens)
        return tagged_entities

    def __get_continuous_tagged_chunks(self, tagged_tokens: List[TaggedEntity]) -> List[TaggedEntity]:
        tagged_tokens_clusters_gen = self.__generate_clusters(tagged_tokens, self.__pred_same_tagged_entity)
        tagged_entities = [TaggedEntity(
            text=" ".join([tagged_token.text for tagged_token in tagged_tokens_cluster]),
            tag=tagged_tokens_cluster[0].tag,
            indx_sentence=tagged_tokens_cluster[0].indx_sentence,
            span_in_sentence=(tagged_tokens_cluster[0].span_in_sentence[0], tagged_tokens_cluster[-1].span_in_sentence[1]))
            for tagged_tokens_cluster in tagged_tokens_clusters_gen]
        return tagged_entities

    def __pred_same_tagged_entity(self, prev_tagged_token: TaggedEntity, curr_tagged_token: TaggedEntity):
        return curr_tagged_token.tag != 'O'

    def __generate_clusters(self, list, pred_same_cluster):
        cluster = []
        prev_elem = None
        for elem in list:
            if not prev_elem or pred_same_cluster(prev_elem, elem):
                cluster.append(elem)
            elif cluster:
                yield cluster
                cluster = []
            prev_elem = elem
        if cluster:
            yield cluster

    def __extract_coreferences_clusters(self, data) -> List[List[CoReference]]:
        return [[CoReference(text=coref['text'],
                             type=coref['type'],
                             plurality=coref['number'],
                             gender=coref['gender'],
                             animacy=coref['animacy'],
                             indx_sentence=coref['sentNum'] - 1,
                             span_in_sentence=(coref['startIndex'] - 1, coref['endIndex'] - 2),
                             is_representative_mention=coref['isRepresentativeMention'])
                 for coref in corefs_cluster]
                for corefs_cluster in data['corefs'].values()]

    def __extract_openie_relations(self, data) -> List[Relation]:
        return [
            Relation(subject=openie_relation['subject'], subject_span_in_sentence=tuple(openie_relation['subjectSpan']),
                     relation_type=openie_relation['relation'], object=openie_relation['object'],
                     object_span_in_sentence=tuple(openie_relation['objectSpan']), )
            for sentence_obj in data['sentences'] for openie_relation in sentence_obj['openie']]


if __name__ == "__main__":
    example_sentence = 'Renya walked him to school everyday. She\'d talk to him about love. Then, once they got to the school, Renya would leave him and go do math alone. Ichi couldn\'t fathom what she was thinking, playing around like that. Ichi knew Reyna was lying to him. Ichi could smell it on her.'
    print('Creating TEE object')
    tee = TextAnalyzer()
    text_analysis = {}
    data = {}
    try:
        print('Executing Text Analysis')
        text_analysis, data = tee.analyze_text(example_sentence)
        print('Finished Text Analysis')
    finally:
        tee.dispose()
    pass