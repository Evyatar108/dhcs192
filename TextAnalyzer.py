from stanfordcorenlp import StanfordCoreNLP
from typing import List
import json

from ObjectModels.TextAnalysis import *


class TextAnalyzer:

    def __init__(self):
        self.nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05')

    def dispose(self):
        self.nlp.close()

    def analyze_text(self,text) -> TextAnalysis:
        data = self.__request_data(text)
        sentences = self.__extract_sentences(data)
        tagged_entities = self.__extract_tagged_entities(data)
        coreferences = self.__extract_coreferences(data)
        return TextAnalysis(data, sentences, tagged_entities, coreferences)


    def __request_data(self, text):
        data_as_text = self.nlp.annotate(text, properties={'annotators': 'coref, ssplit, ner, sentiment', 'outputFormat': 'json'})
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
                tagged_tokens.append(TaggedEntity(text=token['originalText'], tag=token['ner'], indx_sentence= indx, indx_start=token['index'], indx_end=token['index']+1))
        tagged_entities = self.__get_continuous_tagged_chunks(tagged_tokens)
        return tagged_entities

    def __get_continuous_tagged_chunks(self, tagged_tokens: List[TaggedEntity]) -> List[TaggedEntity]:
        tagged_entities = []
        current_tagged_entity = None
        current_tokens = []
        for tagged_entity in tagged_tokens:
            if tagged_entity.tag != "O":
                if not current_tagged_entity:
                    current_tagged_entity = TaggedEntity(\
                        text=None,\
                        tag=tagged_entity.tag,\
                        indx_sentence=tagged_entity.indx_sentence,\
                        indx_start=tagged_entity.indx_start-1,
                        indx_end=None)
                current_tokens.append(tagged_entity.text)
            else:
                if current_tagged_entity:
                    current_tagged_entity.text = " ".join(current_tokens)
                    current_tagged_entity.indx_end = tagged_entity.indx_end-1
                    tagged_entities.append(current_tagged_entity)
                    current_tokens = []
                    current_tagged_entity = None
        if current_tagged_entity:
            current_tagged_entity.text = " ".join(current_tokens)
            current_tagged_entity.indx_end = tagged_tokens[-1].indx_end-1
            tagged_entities.append(current_tagged_entity)
        return tagged_entities

    def __extract_coreferences(self, data) -> List[List[CoReference]]:
        coreferences = []
        for corefs_cluster in data['corefs'].values():
            for coref in corefs_cluster:
                coreferences.append(
                    CoReference(text=coref['text'],
                                type=coref['type'], \
                                plurality=coref['number'], \
                                gender=coref['gender'],
                                animacy=coref['animacy'], \
                                indx_sentence=coref['sentNum'], \
                                indx_start=coref['startIndex'],
                                indx_end=coref['endIndex'],
                                is_representative_mention=coref['isRepresentativeMention'],
                                indx_named_entity=None))
        return coreferences



def main():
    example_sentence = 'Zorian’s eyes abruptly shot open as a sharp pain erupted from his stomach. His whole body convulsed, buckling against the object that fell on him, and suddenly he was wide awake, not a trace of drowsiness in his mind. Georgy University, you should come'
    print('Creating TEE object')
    tee = TextAnalyzer()
    text_analysis = {}
    try:
        print('Extracting tagged entities')
        print('Tagged Entities:')

        text_analysis = tee.analyze_text(example_sentence)
    finally:
        tee.dispose()

if __name__ == "__main__":
    main()



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