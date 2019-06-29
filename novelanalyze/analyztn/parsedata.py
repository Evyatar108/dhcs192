# coding=utf-8
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SentimentedSentence:
    text: str
    sentiment: str
    sentiment_value: int


@dataclass
class TaggedTextEntity:
    text: str
    tag: str
    indx_sentence: int
    span_in_sentence: Tuple[int, int]


@dataclass
class CoReference:
    text: str
    ref_type: str
    plurality: str
    gender: str
    animacy: str
    indx_sentence: int
    span_in_sentence: Tuple[int, int]
    is_representative_mention: bool
    speaker: str


@dataclass
class Relation:
    indx_sentence: int
    subject_name: str
    subject_span_in_sentence: Tuple[int, int]
    relation_str: str
    relation_span: Tuple[int, int]
    object_name: str
    object_span_in_sentence: Tuple[int, int]


@dataclass
class TextAnalysis:
    sentimented_sentences: List[SentimentedSentence]
    tagged_entities: List[TaggedTextEntity]
    coreferences_clusters: List[List[CoReference]]
    relations: List[Relation]
