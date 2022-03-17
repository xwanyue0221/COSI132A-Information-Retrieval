import math
from typing import Any, List
import re

from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore


class TextProcessing:
    def __init__(self, stemmer, stop_words, word_tokenize, *args):
        """
        class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted index.
        :param stemmer:
        :param stop_words:
        :param args:
        """
        self.tokenizer = word_tokenize
        self.stemmer = stemmer
        self.STOP_WORDS = stop_words

    @classmethod
    def from_nltk(cls, stemmer: Any = PorterStemmer().stem, stop_words: List[str] = stopwords.words("english"), word_tokenize: Any = word_tokenize) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer:
        :param stop_words:
        :return:
        """
        return cls(stemmer, set(stop_words), word_tokenize)

    def normalize(self, token: str) -> str:
        """
        normalize the token based on:
        1. make all characters in the token to lower case
        2. remove any characters from the token other than alphanumeric characters and dash ("-")
        3. after step 1, if the processed token appears in the stop words list or its length is 1, return an empty string
        4. after step 1, if the processed token is NOT in the stop words list and its length is greater than 1, return the stem of the token
        :param token:
        :return:
        """
        lowerCase = token.lower().strip()
        cleanText = re.sub(r'[^-\w]', '', lowerCase)
        stop_words = set(self.STOP_WORDS)

        if (cleanText not in stop_words) and (len(cleanText) > 1):
            return self.stemmer(cleanText)
        else:
            return ""

    def get_normalized_tokens(self, title: str, content: str) -> List[str]:
        """
        pass in the title and content_str of each document, and return a list of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first.
        Note that you don't want to remove duplicate tokens as what you did in HW3, because it will later be used to compute term frequency
        :param title:
        :param content:
        :return:
        """
        titleTokens = self.tokenizer(title)
        normTitle = [self.normalize(item) for item in titleTokens if self.normalize(item) != ""]

        contentTokens = self.tokenizer(content)
        normContent = [self.normalize(each) for each in contentTokens if self.normalize(each) != ""]

        AllTokens = normTitle + normContent
        return AllTokens

    @staticmethod
    def idf(N: int, df: int) -> float:
        """
        compute the logarithmic (base 2) idf score
        :param N: document count N
        :param df: document frequency
        :return:
        """
        if N > 0.0 and df > 0.0:
            return float(math.log2(N/df))
        else:
            return 0.0

    @staticmethod
    def tf(freq: int) -> float:
        """
        compute the logarithmic tf (base 2) score
        :param freq: raw term frequency
        :return:
        """
        if freq > 0:
            return float(1 + math.log2(freq))
        else:
            return 0.0

if __name__ == "__main__":
    pass
