from typing import List


class SentimentedSentence:
    def __init__(self, text, sentiment):
        self.text = text
        self.sentiment = sentiment


class TaggedEntity:
    def __init__(self, text, tag, indx_sentence, indx_word_start, indx_word_end):
        self.text = text
        self.tag = tag
        self.indx_sentence = indx_sentence
        self.indx_word_start = indx_word_start
        self.indx_word_end = indx_word_end


class CoReference:
    def __init__(self, text, type, plurality, gender, animacy, indx_sentence, indx_word_start, indx_word_end,
                 is_representative_mention):
        self.text = text
        self.type = type
        self.plurality = plurality
        self.gender = gender
        self.animacy = animacy
        self.indx_sentence = indx_sentence
        self.indx_word_start = indx_word_start
        self.indx_word_end = indx_word_end
        self.is_representative_mention = is_representative_mention

class TextAnalysis:
    def __init__(self, sentimented_sentences: List[SentimentedSentence], tagged_entities: List[TaggedEntity],
                 coreferences_clusters: List[List[CoReference]]):
        self.sentimented_sentences = sentimented_sentences
        self.tagged_entities = tagged_entities
        self.coreferences_clusters = coreferences_clusters

