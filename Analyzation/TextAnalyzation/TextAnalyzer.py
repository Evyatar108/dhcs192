from stanfordcorenlp import StanfordCoreNLP
import json

from Analyzation.TextAnalyzation.TextAnalysis import *


class TextAnalyzer:

    def __init__(self):
        self.nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05')

    def dispose(self):
        self.nlp.close()

    def analyze_text(self,text) -> TextAnalysis:
        data = self.__request_data(text)
        sentences = self.__extract_sentimented_sentences(data)
        tagged_entities = self.__extract_tagged_entities(data)
        coreferences_clusters = self.__extract_coreferences_clusters(data)
        return (TextAnalysis(sentences, tagged_entities, coreferences_clusters), data)


    def __request_data(self, text):
        data_as_text = self.nlp.annotate(text, properties={'annotators': 'coref, ssplit, ner, sentiment, kbp', 'outputFormat': 'json'})
        return json.loads(data_as_text)

    def __extract_sentimented_sentences(self,data) -> List[SentimentedSentence]:
        sentimented_sentences = []
        for sentence_obj in data['sentences']:
            text = "".join([token['originalText'] + token['after'] for token in sentence_obj['tokens']])
            sentiment = sentence_obj['sentiment']
            sentimented_sentences.append(SentimentedSentence(text=text, sentiment=sentiment))
        return sentimented_sentences


    def __extract_tagged_entities(self, data) -> List[TaggedEntity]:
        tagged_tokens = []
        for indx,s in enumerate(data['sentences']):
            for token in s['tokens']:
                tagged_tokens.append(TaggedEntity(text=token['originalText'], tag=token['ner'], indx_sentence= indx, indx_word_start=token['index']-1, indx_word_end=token['index']))
        tagged_entities = self.__get_continuous_tagged_chunks(tagged_tokens)
        return tagged_entities

    def __get_continuous_tagged_chunks(self, tagged_tokens: List[TaggedEntity]) -> List[TaggedEntity]:
        tagged_tokens_clusters_gen = self.__generate_clusters(tagged_tokens, self.__pred_same_tagged_entity)
        tagged_entities = [TaggedEntity( \
            text=" ".join([tagged_token.text for tagged_token in tagged_tokens_cluster]), \
            tag=tagged_tokens_cluster[0].tag, \
            indx_sentence=tagged_tokens_cluster[0].indx_sentence, \
            indx_word_start=tagged_tokens_cluster[0].indx_word_start,
            indx_word_end=tagged_tokens_cluster[-1].indx_word_end)
            for tagged_tokens_cluster in tagged_tokens_clusters_gen]
        return tagged_entities


    def __pred_same_tagged_entity(self, prev_tagged_token: TaggedEntity, curr_tagged_token: TaggedEntity):
        return curr_tagged_token.tag != 'O'

    def __generate_clusters(self,list,pred_same_cluster):
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
                             type=coref['type'], \
                             plurality=coref['number'], \
                             gender=coref['gender'],
                             animacy=coref['animacy'], \
                             indx_sentence=coref['sentNum'], \
                             indx_word_start=coref['startIndex'],
                             indx_word_end=coref['endIndex'],
                             is_representative_mention=coref['isRepresentativeMention'])
                 for coref in corefs_cluster]
                for corefs_cluster in data['corefs'].values()]





if __name__ == "__main__":
    example_sentence = 'John is living in Tranko, the largest city in the world' # 'Zorian’s eyes abruptly shot open as a sharp pain erupted from his stomach. His whole body convulsed, buckling against the object that fell on him, and suddenly he was wide awake, not a trace of drowsiness in his mind. Georgy University, you should come'
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

# sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
# print('Tokenize:', nlp.word_tokenize(sentence))
# print('Part of Speech:', nlp.pos_tag(sentence))



#
#
# print('Named Entities:', nlp.ner(sentence))
#
# print('Continues Named Entities:', get_continuous_chunks(named_entities))
#
# nlp.close() # Do not forget to close! The backend server will consume a lot memery.