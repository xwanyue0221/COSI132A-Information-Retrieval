import re
from typing import Union, List, Tuple, Iterable
from utils import timer
from collections import defaultdict

from text_processing import TextProcessing
from customized_text_processing import CustomizedTextProcessing
from mongo_db import insert_db_index, query_db_index

# Initialize text processor object
text_processor = TextProcessing.from_nltk()
custom_text_processor = CustomizedTextProcessing.from_customized()


@timer
def build_inverted_index(wapo_docs: Iterable, custom_processor: bool) -> None:
    """
    "load wapo_pa3.jl to build the inverted index and insert the index by using mongo_db.insert_db_index method"
    :param wapo_docs: a generator which contains all the essential information of the document collections
    :return: None
    """
    if custom_processor:
        processor = custom_text_processor
    else:
        processor = text_processor

    wapoDocs = list(wapo_docs)
    print("inverted index wapoDocs", len(wapoDocs))
    inverted_Index = defaultdict(list)
    for each in wapoDocs:
        value = list(processor.get_normalized_tokens(each["title"], each["content_str"]))
        for term in value:
            inverted_Index[term].append(each["id"])
    index_list = list(map(lambda kv: {"token":kv[0], "doc_ids":kv[1]}, inverted_Index.items()))
    insert_db_index(index_list)


def intersection(posting_lists: List[List[int]]) -> List[int]:
    """
    implementation of the intersection of a list of posting lists that have been ordered from the shortest to the longest
    :param posting_lists: a list includes several list consisting of doc id token term appears inside
    :return: a list includes the id of documents that includes the all the query token
    """
    if len(posting_lists) == 0:
        return []
    else:
        return list(set.intersection(*[set(x) for x in posting_lists]))


def query_inverted_index(query: str, custom_processor: bool) -> Tuple[List[int], List[str], List[str]]:
    """
    conjunctive query over the built index by using mongo_db.query_db_index method
    return a list of matched document ids, a list of stop words and a list of unknown words separately
    :param query: user input query
    :return: return a list of matched document ids, a list of stop words, and a list of unknown words
    """
    if custom_processor:
        processor = custom_text_processor
    else:
        processor = text_processor

    queryIndexs = []
    unknownToken = []
    sw = set(processor.STOP_WORDS)
    # rmStopWords = [x for x in processor.tokenizer(query.lower()) if x in sw]
    rmStopWords = [x for x in query.lower().split(" ") if x in sw]
    print("rmStopWords", rmStopWords, query.lower().split(" "))

    # normalized_query = processor.get_normalized_tokens(query, '')
    query_split = query.lower().split(" ")
    normalized_query = [processor.normalize(item) for item in query_split]
    normalized_query = [each for each in normalized_query if each != ""]
    normalized_query = set(normalized_query)
    print("normalized_query ", normalized_query, custom_processor)

    for token in normalized_query:
        result = query_db_index(token)
        if result != None:
            queryIndexs.append(result["doc_ids"])
        else:
            unknownToken.append(token)
    return queryIndexs, rmStopWords, unknownToken

if __name__ == "__main__":
    pass
