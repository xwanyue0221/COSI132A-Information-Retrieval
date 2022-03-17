import math
import heapq
from typing import List, Tuple, Dict, Iterable, DefaultDict
from utils import timer
from collections import Counter
from collections import defaultdict
from text_processing import TextProcessing

from pathlib import Path
from utils import load_wapo
from mongo_db import insert_vs_index, insert_doc_len_index, query_vs_index, query_doc_len_index

text_processor = TextProcessing.from_nltk()


def get_doc_vec_norm(term_tfs: List[float]) -> float:
    """
    helper function, should be called in build_inverted_index; compute the length of a document vector
    :param term_tfs: a list of term weights (log tf) for one document
    :return:
    """
    sumTF = sum(map(lambda x: x ** 2, term_tfs))
    if sumTF:
        return float(math.sqrt(sumTF))
    else:
        return 0.0


def compute_cosine(query_vector:float, doc_vector:float, doc_length: float) -> float:
    """
    :param query_vector: a float variables which represents the tf-idf weight of the all the valid tokens in the query
    :param doc_vector: a float variables which represents the tf-idf weight of the all the valid tokens in the document
    :param doc_vector: a float variables which represents the length of the all the valid tokens in the document
    :return: a float
    """
    return (query_vector * doc_vector)/doc_length


@timer
def build_inverted_index(wapo_docs: Iterable,) -> None:
    """
    load wapo_pa4.jl to build two indices:
        - "vs_index": for each normalized term as a key, the value should be a list of tuples; each tuple stores the doc id this term appear in and the term weight (log tf)
        - "doc_len_index": for each doc id as a key, the value should be the "length" of that document vector
    insert the indices by using mongo_db.insert_vs_index and mongo_db.insert_doc_len_index method
    """
    # global total_Doc
    wapoDocs = list(wapo_docs)
    total_Doc = len(wapoDocs)
    print("wapoDocs total number: ", total_Doc)

    # forming vs_index list
    inverted_Index = defaultdict(list)
    vs_index = {}
    for each in wapoDocs:
        allTokens = text_processor.get_normalized_tokens(each["title"], each["content_str"])
        for term in allTokens:
            inverted_Index[term].append((each["id"]))

    for each in inverted_Index.items():
        vs_index.update({each[0]:[(item[0], text_processor.tf(item[1])) for item in Counter(each[1]).items()]})
    index_list = [{'term':item, 'term_tf': vs_index[item]} for item in vs_index]
    insert_vs_index(index_list)

    # forming doc_vec list
    doc_vec = defaultdict(list)
    for term in index_list:
        for tup in term['term_tf']:
            doc_vec[tup[0]].append(tup[1])
    doc_list = [{'doc_id':item, 'length': get_doc_vec_norm(doc_vec[item])} for item in doc_vec]
    insert_doc_len_index(doc_list)


def parse_query(query: str) -> Tuple[List[str], List[str], List[str]]:
    """
    helper function, should be called in query_inverted_index
    given each query, return a list of normalized terms, a list of stop words and a list of unknown words separately
    """
    unknownToken = []
    sw = set(text_processor.STOP_WORDS)
    rmStopWords = [x for x in query.lower().split(" ") if x in sw]
    print("rmStopWords", rmStopWords, query.lower().split(" "))

    query_split = query.lower().split(" ")
    normalized_query = [text_processor.normalize(item) for item in query_split]
    normalized_query = [each for each in normalized_query if each != ""]
    return normalized_query, rmStopWords, unknownToken


def top_k_docs(doc_scores: Dict[int, float], k: int) -> List[Tuple[float, int]]:
    """
    helper function, should be called in query_inverted_index method
    given the doc_scores, return top k doc ids and corresponding scores using a heap
    :param doc_scores: a dictionary where doc id is the key and cosine similarity score is the value
    :param k:
    :return: a list of tuples, each tuple contains (score, doc_id)
    """
    scores_list = [(sum(doc_scores[each]), each) for each in doc_scores]
    heapq.heapify(scores_list)
    heap_result = heapq.nlargest(k, scores_list, key=lambda x: x[0])
    return heap_result


def query_inverted_index(query:str, k:int, total_Doc:int) -> Tuple[List[Tuple[float, int]], List[str], List[str], List[Tuple[str, float]], DefaultDict]:
    """
    disjunctive query over the vs_index with the help of mongo_db.query_vs_index, mongo_db.query_doc_len_index methods
    return a list of matched documents (output from the function top_k_docs), a list of stop words and a list of unknown words separately
    """
    query_term, stop_words, unknown_list = parse_query(query)

    doc_scores = defaultdict(list)
    query_set = set(query_term)
    query_vec = 0
    query_report = defaultdict(list)
    doc_report = defaultdict(list)
    doc_vec = defaultdict(list)

    if query_set: # query_term is not a null set
        for token in query_set:
            result = query_vs_index(token)
            if result is None:
                unknown_list.append(token)
            else:
                # calculate the query log tf
                term_df = result['term_tf']
                term_tf = text_processor.tf(query_term.count(token))
                term_idf = text_processor.idf(total_Doc, len(term_df))
                query_report[token].append(term_idf)
                term_weight = term_tf * term_idf
                query_vec += term_weight
        # calculate the corresponding log tf for each document
                for doc_ in term_df:
                    doc_vec[doc_[0]].append(doc_[1])
                    doc_report[doc_[0]].append(token)

        sorted_doc_vec = sorted([(each, sum(doc_vec[each])) for each in doc_vec], key=lambda x: x[0])
        # compute the cosine similarity score between the query and document that contains token(s) appearing in the query
        for each in sorted_doc_vec:
            cos_score = compute_cosine(query_vec, each[1], query_doc_len_index(each[0])['length'])
            doc_scores[each[0]].append(cos_score)

    # filtering out the top k documents
    top_k = top_k_docs(doc_scores, k)
    query_report = [(each, query_report[each]) for each in query_report]
    return top_k, stop_words, unknown_list, query_report, doc_report


if __name__ == "__main__":
    pass
    # k = 2
    # DATA_DIR = Path(__file__).parent.joinpath("pa4_data")
    # wapo_path = DATA_DIR.joinpath("wapo_test.jl")
    # wapo_docs = load_wapo(wapo_path)  # load and process WAPO documents
    # print(build_inverted_index(wapo_docs))
    # print(query_inverted_index("Get to part the new part token", k))