from typing import Dict, List, Iterable

import pymongo

client = pymongo.MongoClient("localhost", 27017)  # connect to the mongodb server running on your localhost
db = client["ir_2022_wapo"]  # create a new database called "ir_2022_wapo"


def drop(dbName:str) -> None:
    if dbName in db.list_collection_names():
        db[dbName].drop()


def insert_docs(docs: Iterable) -> None:
    """
    - create a collection called "wapo_docs" (done)
    - add a unique ascending index on the key "id"
    - insert documents into the "wapo_docs" collection
    :param docs: WAPO docs iterator (utils.load_wapo(...))
    :return: None
    """
    wapo_collection = db["wapo_docs"]
    wapo_collection.create_index([('id', pymongo.ASCENDING)])
    wapo_collection.insert_many(docs)


def insert_db_index(index_list: List[Dict]) -> None:
    """
    - create a collection called "inverted_index"
    - add a unique ascending index on the key "token"
    - insert posting lists (index_list) into the "inverted_index" collection
    :param index_list: posting lists in the format of [{"token": "post", "doc_ids": [0, 3, 113, 444, ...]}, {...}, ...]
    :return: None
    """
    index_collection = db["inverted_index"]
    index_collection.create_index([('token', pymongo.ASCENDING)])
    index_collection.insert_many(index_list)


def query_doc(doc_id: int) -> Dict:
    """
    query the document from "wapo_docs" collection based on the doc_id
    :param doc_id: an integer which represents the id of a document
    :return: a dictionary object which stores detailed information regarding a document
    """
    return db["wapo_docs"].find_one({"id":doc_id}, {'_id': 0})
    # return db["wapo_docs"].find_one({"id":doc_id}, {'_id': 0})
    # list(db["wapo_docs"].find({"id":{"$in":doc_id}}, {'_id': 0}))


def query_db_index(token: str) -> Dict:
    """
    query the posting list from "inverted_index" collection based on the token
    :param token: a string object which represents a word or a term
    :return: a dictionary object which stores detailed information regarding a term
    """
    return db["inverted_index"].find_one({"token": token}, {'_id': 0})
