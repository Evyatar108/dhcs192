from Analyzation.content_provider_base import ContentProviderBase
from Analyzation.PostAnalysisProcessing import post_analysis_processing
from Analyzation.PostAnalysisProcessing.ObjectModels.novel_data import NovelEntities
from Analyzation.TextAnalyzation.text_analyzation import TextAnalyzer


def analyize_book(book_content_provider: ContentProviderBase) -> NovelEntities:
    chapters_generator = book_content_provider.generate_all_chapters()
    novel_entities = NovelEntities()
    text_analyzer = TextAnalyzer()
    try:
        for indx_chapter, chapter in enumerate(chapters_generator):
            text_analysis = text_analyzer.analyze_text(chapter)
            post_analysis_processing.process_text_analysis(text_analysis, novel_entities, indx_chapter)
    finally:
        text_analyzer.dispose()

    return novel_entities
