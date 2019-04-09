# coding=utf-8
from typing import List, Tuple


class SentimentedSentence:
    def __init__(self, text, sentiment, sentiment_value):
        self.text = text
        self.sentiment = sentiment
        self.sentiment_value = sentiment_value


class TaggedTextEntity:
    def __init__(self, text, tag, indx_sentence, span_in_sentence):
        self.text = text
        self.tag = tag
        self.indx_sentence = indx_sentence
        self.span_in_sentence = span_in_sentence


class CoReference:
    def __init__(self, text, ref_type, plurality, gender, animacy, indx_sentence, span_in_sentence,
                 is_representative_mention):
        self.text = text
        self.ref_type = ref_type
        self.plurality = plurality
        self.gender = gender
        self.animacy = animacy
        self.indx_sentence = indx_sentence
        self.span_in_sentence = span_in_sentence
        self.is_representative_mention = is_representative_mention


class Relation:
    def __init__(self, indx_sentence: int, subject_name: str, subject_span_in_sentence: Tuple[int, int],
                 relation_str: str, object_name: str, object_span_in_sentence: Tuple[int, int]):
        self.indx_sentence = indx_sentence
        self.subject_name = subject_name
        self.subject_span_in_sentence = subject_span_in_sentence
        self.relation_str = relation_str
        self.object_name = object_name
        self.object_span_in_sentence = object_span_in_sentence


class TextAnalysis:
    def __init__(self, sentimented_sentences: List[SentimentedSentence], tagged_entities: List[TaggedTextEntity],
                 coreferences_clusters: List[List[CoReference]], relations: List[Relation]):
        self.sentimented_sentences = sentimented_sentences
        self.tagged_entities = tagged_entities
        self.coreferences_clusters = coreferences_clusters
        self.relations = relations
