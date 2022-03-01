import re
from typing import Set, Any, List
from pathlib import Path
from utils import load_wapo

from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore


class TextProcessing:
    def __init__(self, stemmer, stop_words, word_tokenize, *args):
        """
        class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted index.
        :param stemmer: Porter Stemmer from NLTK library
        :param stop_words: stopwords list from NLTK library
        :param word_tokenize: word tokenize from NLTK library
        :param args:
        """
        self.tokenizer = word_tokenize
        self.stemmer = stemmer
        self.STOP_WORDS = stop_words

    @classmethod
    def from_nltk(cls, stemmer: Any = PorterStemmer().stem, stop_words: List[str] = stopwords.words("english"), word_tokenize: Any = word_tokenize) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer: Porter Stemmer from NLTK library
        :param stop_words: stopwords list from NLTK library
        :param word_tokenize: word tokenize from NLTK library
        :return:
        """
        return cls(stemmer, set(stop_words), word_tokenize)

    def normalize(self, token: str) -> str:
        """
        normalize the token based on:
        1. make all characters in the token to lower case (done)
        2. remove any characters from the token other than alphanumeric characters and dash ("-") (done)
        3. after step 2, if the processed token appears in the stop words list or its length is 1, return an empty string
        4. after step 2, if the processed token is NOT in the stop words list and its length is greater than 1, return the stem of the token
        :param token: a term that appears in a document
        :return: the normalized version of token or empty string if the token is in stop words list or its length is 1
        """
        lowerCase = token.lower().strip()
        cleanText = re.sub(r'[^-\w]', '', lowerCase)
        stop_words = set(self.STOP_WORDS)

        if (cleanText not in stop_words) and (len(cleanText) > 1):
            return self.stemmer(cleanText)
        else:
            return ""


    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first
        :param title: a string represents the title of a document
        :param content:  a string includes the content of a document
        :return: a set of unique token
        """
        titleTokens = self.tokenizer(title)
        normTitle = [self.normalize(item) for item in titleTokens if self.normalize(item) != ""]

        contentTokens = self.tokenizer(content)
        normContent = [self.normalize(each) for each in contentTokens if self.normalize(each) != ""]

        AllTokens = set(normTitle + normContent)
        return AllTokens


if __name__ == "__main__":
    pass
    # DATA_DIR = Path(__file__).parent.joinpath("pa3_data")
    # wapo_path = DATA_DIR.joinpath("wapo_pa2.jl")
    # wapo_docs = load_wapo(wapo_path)  # load and process WAPO documents
    # stop_words = stopwords.words("english")
    # tp = TextProcessing(PorterStemmer, stop_words)
    # print(tp.get_normalized_tokens(test["title"], test["content_str"]))
