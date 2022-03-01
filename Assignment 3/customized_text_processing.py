import re
import ast
from pathlib import Path
from utils import load_wapo
from typing import Set, Any, List, Dict
from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
# from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords  # type: ignore

# read contraction dictionary from a plain text file
data_dir = Path(__file__).parent.joinpath("pa3_data")
contraction_path = data_dir.joinpath("dict.txt")
with open(contraction_path) as f:
    data = f.read()
dictionary = {}
for each in data.split(","):
    key, value = each.split(":")
    key = key.strip()
    value = value.strip()
    dictionary.update({key:value})
f.close()

class CustomizedTextProcessing:
    def __init__(self, stemmer, stop_words, contraction_dict, word_tokenize, *args, **kwargs):
        """
        the default TextProcessing class uses Porter stemmer and stopwords list from nltk to process tokens.
        in the Python class, please include at least one other approach for each of the following:
        - to identify a list of terms that should also be ignored along with stopwords ("1")
        - to normalize tokens other than stemming and lemmatization

        Your implementation should be in this class. Create more helper functions as you needed. Your approaches could
        be based on heuristics, the usage of a tool from nltk or some new feature you implemented using Python. Be creative!

        :param args:
        :param kwargs:
        """
        new_stopwords = ["all", "almost", "along", "already", "also", "although", "always", "among", "anyhow", "anymore", "amongst",
                         "amoungst", "anyway", "anyways", "however", "thou", "though", "wherever", "meanwhile", "moreover"]

        self.stemmer = stemmer
        self.STOP_WORDS = stop_words
        self.STOP_WORDS.update(new_stopwords)
        self.contraction_dict = contraction_dict
        self.tokenizer = word_tokenize

    @classmethod
    def from_customized(cls, stemmer: Any = PorterStemmer().stem, stop_words: List[str] = stopwords.words("english"),
                        contraction_dic: Dict = dictionary, word_tokenize: Any = word_tokenize) -> "CustomizedTextProcessing":
        """
        You don't necessarily need to implement a class method, but if you do, please use this boilerplate.
        :param args:
        :param kwargs:
        :return:
        """
        return cls(stemmer, set(stop_words), contraction_dic, word_tokenize)

    def expand_contraction(self, s:str, contractions_dict: Dict) -> str:
        """
        expand all contraction expressions, such as expanding phrase of "you'll" to "you will"
        :param s: a string
        :param contractions_dict: a dictionary stores key value pairs about expression of contraction expansion
        :return: a expanded expression or token itself if it could not be found in the dictionary
        """
        contractions_re = re.compile('(%s)'%'|'.join(contractions_dict.keys()))
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, s)

    def normalize(self, token: str) -> str:
        """
        your approach to normalize a token. You can still adopt the criterion and methods from TextProcessing along with your own approaches
        :param token: a term that appears in the document
        :return: the normalized version of token or empty string if the token is in stop words list or its length is 1
        """

        # acronym = re.findall(r'[a-z](?:[.|&]+[a-z])[.|&]?', token)
        # find acronym such as "U.S. and U.K."
        if re.findall(r'[a-z](?:[.|&]+[a-z])[.|&]?', token):
            return token
        # find other acronyms such as "vs."
        elif re.findall(r'(?:[a-z]+[.|&]+)[a-z]?', token):
            return token
        else:
            # striping all spaces
            lowerCase = token.strip()
            # remove all emojis
            emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"
                                       u"\U0001F300-\U0001F5FF"
                                       u"\U0001F680-\U0001F6FF"
                                       u"\U0001F1E0-\U0001F1FF"
                                       "]+", flags=re.UNICODE)
            cleanText = emoji_pattern.sub(r'', lowerCase)
            # remove all characters other than alphanumeric characters and dash
            cleanText = re.sub(r'[^-\w]', '', cleanText)
            # remove stop words
            stop_words = set(self.STOP_WORDS)
            if (cleanText not in stop_words) and (len(cleanText) > 1):
                return self.stemmer(cleanText)
            else:
                return ""

    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        :param title: a string represents the title of a document
        :param content:  a string includes the content of a document
        :return: a set of unique token
        """

        # expand contraction phrases
        # title_result = self.expand_contraction(title.lower(), self.contraction_dict)
        titleTokens = self.tokenizer(title.lower())
        normTitle = [self.normalize(item) for item in titleTokens]
        normTitle = [each for each in normTitle if each != ""]

        # content_result = self.expand_contraction(content.lower(), self.contraction_dict)
        contentTokens = self.tokenizer(content.lower())
        normContent = [self.normalize(item) for item in contentTokens if self.normalize(item) != ""]
        normContent = [each for each in normContent if each != ""]

        AllTokens = set(normTitle + normContent)
        return AllTokens

if __name__ == "__main__":
    pass

