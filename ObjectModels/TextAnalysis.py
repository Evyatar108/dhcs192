class TextAnalysis:
    def __init__(self,original_data, sentimented_sentences, tagged_entities, coreferences):
        self.original_data = original_data
        self.sentimented_sentences = sentimented_sentences
        self.tagged_entities = tagged_entities
        self.coreferences = coreferences

class SentimentedSentence:
    def __init__(self, text, sentiment):
        self.text = text
        self.sentiment = sentiment

class TaggedEntity:
    def __init__(self, text, tag, indx_sentence, indx_start, indx_end):
        self.text = text
        self.tag = tag
        self.indx_sentence = indx_sentence
        self.indx_start = indx_start
        self.indx_end = indx_end

class CoReference:
    def __init__(self, text, type, plurality, gender, animacy, indx_sentence, indx_start, indx_end, is_representative_mention, indx_named_entity):
        self.text = text
        self.type = type
        self.plurality = plurality
        self.gender = gender
        self.animacy = animacy
        self.indx_sentence = indx_sentence
        self.indx_start = indx_start
        self.indx_end = indx_end
        self.is_representative_mention = is_representative_mention
        self.indx_named_entity = indx_named_entity