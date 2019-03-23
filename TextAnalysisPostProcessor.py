from ObjectModels.TextAnalysis import *


class TextAnalysisPostProcessor:
    def __init__(self):
        pass

    def process_text_analysis(self, text_analysis: TextAnalysis):
        self.__process_coreferences(text_analysis)

    def __process_coreferences(self,text_analysis):
        pass


if __name__ == "__main__":
    pass
