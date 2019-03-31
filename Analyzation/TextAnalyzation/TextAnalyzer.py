import itertools
from typing import Dict

from stanfordcorenlp import StanfordCoreNLP
import json

from Analyzation.TextAnalyzation.RelationNormalizer import RelationNormalizer
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
        data_as_text = self.nlp.annotate(text, properties={'annotators': 'coref, tokenize,ssplit, ner, sentiment, openie, kbp, pos, lemma, parse',
                                                           'outputFormat': 'json',
                                                           'coref.algorithm': 'neural',
                                                           'timeout': '50000'})
        return json.loads(data_as_text)

    def __extract_sentimented_sentences(self, data) -> List[SentimentedSentence]:
        sentimented_sentences = []
        for sentence_obj in data['sentences']:
            text = "".join([token['originalText'] + token['after'] for token in sentence_obj['tokens']])
            sentiment = sentence_obj['sentiment']
            sentimented_sentences.append(SentimentedSentence(text=text, sentiment=sentiment, sentiment_value=
            int(sentence_obj['sentimentValue']) - 2))
        return sentimented_sentences

    def __extract_tagged_entities(self, data) -> List[TaggedTextEntity]:
        tagged_tokens = []
        for indx, s in enumerate(data['sentences']):
            for token in s['tokens']:
                tagged_tokens.append(TaggedTextEntity(text=token['originalText'], tag=token['ner'], indx_sentence=indx,
                                                      span_in_sentence=(token['index'] - 1, token['index'] - 1)))
        tagged_entities = self.__get_continuous_tagged_chunks(tagged_tokens)
        return tagged_entities

    def __get_continuous_tagged_chunks(self, tagged_tokens: List[TaggedTextEntity]) -> List[TaggedTextEntity]:
        tagged_tokens_clusters_gen = self.__generate_clusters(tagged_tokens, self.__pred_same_tagged_entity)
        tagged_entities = [TaggedTextEntity(
            text=" ".join([tagged_token.text for tagged_token in tagged_tokens_cluster]),
            tag=tagged_tokens_cluster[0].tag,
            indx_sentence=tagged_tokens_cluster[0].indx_sentence,
            span_in_sentence=(
            tagged_tokens_cluster[0].span_in_sentence[0], tagged_tokens_cluster[-1].span_in_sentence[1]))
            for tagged_tokens_cluster in tagged_tokens_clusters_gen]
        return tagged_entities

    def __pred_same_tagged_entity(self, prev_tagged_token: TaggedTextEntity, curr_tagged_token: TaggedTextEntity):
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
        relations = [
            Relation(indx_sentence=sentence_obj['index'], subject=raw_relation['subject'],
                     subject_span_in_sentence=tuple(raw_relation['subjectSpan']),
                     relation_str=raw_relation['relation'], object=raw_relation['object'],
                     object_span_in_sentence=tuple(raw_relation['objectSpan']), )
            for sentence_obj in data['sentences'] for raw_relation in itertools.chain(sentence_obj['openie'], sentence_obj['kbp'])]

        normalized_relations = map(RelationNormalizer.Normalize, relations)
        return normalized_relations

if __name__ == "__main__":
    # # "Israel is a nice place"  # 'Renya walked him to school everyday. She\'d talk to him about love. Then, once they got to the school, Renya would leave him and go do math alone. Ichi couldn\'t fathom what she was thinking, playing around like that. Ichi knew Reyna was lying to him. Ichi could smell it on her.'

    example_sentence = 'Ron and Anny are father and son' # 'Zorian’s eyes abruptly shot open as a sharp pain erupted from his stomach. His whole body convulsed, buckling against the object that fell on him, and suddenly he was wide awake, not a trace of drowsiness in his mind. “Good morning, brother!” an annoyingly cheerful voice sounded right on top of him. “Morning, morning, MORNING!!!” Zorian glared at his little sister, but she just smiled back at him cheekily, still sprawled across his stomach. She was humming to herself in obvious satisfaction, kicking her feet playfully in the air as she studied the giant world map Zorian had tacked to the wall next to his bed. Or rather, pretended to study – Zorian could see her watching him intently out of the corner of her eyes for a reaction. This was what he got for not arcane locking the door and setting up a basic alarm perimeter around his bed. “Get off,” he told her in the calmest voice he could muster. “Mom said to wake you up,” she said matter-of-factly, not budging from her spot. “Not like this, she didn’t,” Zorian grumbled, swallowing his irritation and patiently waiting till she dropped her guard. Predictably, Kirielle grew visibly agitated after only a few moments of this pretend disinterest. Just before she could blow up, Zorian quickly grasped her legs and chest and flipped her over the edge of the bed. She fell to the floor with a thud and an indignant yelp, and Zorian quickly jumped to his feet to better respond to any violence she might decide to retaliate with. He glanced down on her and sniffed disdainfully. “I’ll be sure to remember this the next time I’m asked to wake you up.”'
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
