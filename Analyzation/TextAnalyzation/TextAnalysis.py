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
    def __init__(self, text, type, plurality, gender, animacy, indx_sentence, span_in_sentence,
                 is_representative_mention):
        self.text = text
        self.type = type
        self.plurality = plurality
        self.gender = gender
        self.animacy = animacy
        self.indx_sentence = indx_sentence
        self.span_in_sentence = span_in_sentence
        self.is_representative_mention = is_representative_mention


class Relation:
    def __init__(self,indx_sentence: int, subject: str, subject_span_in_sentence: Tuple[int, int], relation_type: str, object: str, object_span_in_sentence: Tuple[int, int]):
        self.indx_sentence = indx_sentence
        self.subject = subject
        self.subject_span_in_sentence = subject_span_in_sentence
        self.relation_type = relation_type
        self.object = object
        self.object_span_in_sentence = object_span_in_sentence

class TextAnalysis:
    def __init__(self, sentimented_sentences: List[SentimentedSentence], tagged_entities: List[TaggedTextEntity],
                 coreferences_clusters: List[List[CoReference]], relations: List[Relation]):
        self.sentimented_sentences = sentimented_sentences
        self.tagged_entities = tagged_entities
        self.coreferences_clusters = coreferences_clusters
        self.relations = relations

