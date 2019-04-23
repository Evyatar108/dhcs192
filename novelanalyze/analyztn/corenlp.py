# coding=utf-8
import gzip
import json
import os

from stanfordcorenlp import StanfordCoreNLP

cached_results_file_name = 'cached_results.json.gz'
is_caching_enabled = True


def query_model(text):
    results_dict = {}
    if os.path.isfile(cached_results_file_name):
        with gzip.open(filename=cached_results_file_name, mode='rt') as cache_file:
            results_dict = json.loads(cache_file.read())
    if text not in results_dict:
        __update_results_dict(results_dict, text)

    return results_dict[text]


def __update_results_dict(results_dict, text):
    nlp = StanfordCoreNLP(r'../stanford-corenlp-full-2018-10-05')
    try:
        data_as_text = nlp.annotate(text, properties={
            'annotators': 'coref, tokenize,ssplit, ner, sentiment, openie, kbp, pos, lemma, parse',
            'outputFormat': 'json',
            'coref.algorithm': 'neural',
            'timeout': '50000'})
    finally:
        nlp.close()

    results_dict[text] = json.loads(data_as_text)

    if is_caching_enabled:
        with gzip.open(filename=cached_results_file_name, mode='wt+') as cache_file:
            cache_file.write(json.dumps(results_dict))

    return results_dict
