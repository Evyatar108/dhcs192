# coding=utf-8
import json

from stanfordcorenlp import StanfordCoreNLP


def query_model(text):
    nlp = StanfordCoreNLP(r'../stanford-corenlp-full-2018-10-05')
    try:
        data_as_text = nlp.annotate(text, properties={
            'annotators': 'coref, tokenize,ssplit, ner, sentiment, openie, kbp, pos, lemma, parse',
            'outputFormat': 'json',
            'coref.algorithm': 'neural',
            'timeout': '50000'})
    finally:
        nlp.close()
    return json.loads(data_as_text)
