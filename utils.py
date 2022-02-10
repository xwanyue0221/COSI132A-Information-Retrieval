import os
import re
import json
from typing import Dict, Union, Tuple

def title_match(query: str, title: str) -> bool:
    """
    query: a string object which corresponds to user's search query
    title: a string object which corresponds to each document's unique id
    return: if the document contains any tokens or terms that are included in the search query
    """
    content = [each.lower() for each in title.split(" ")]
    query_token = [each.lower() for each in query.split(" ")]
    result = [x for x in content if x in query_token]
    if len(result) != 0:
        return True
    else:
        return False

def get_snippet(id: str, doc_dict: Dict) -> Tuple:
    """
    id: a string object which corresponds to each document's unique id
    doc_dict: a dict object which includes all essential elements possessed by a document
    return: a tuple object which includes three elements, including document unique id, document's title, and the first 150 characters of this document content
    """
    CLEANR = re.compile('<.*?>')
    title = doc_dict[id]['title']
    content = doc_dict[id]['content_str']
    cleantext = re.sub(CLEANR, '', content)
    return id, title, cleantext[:150]+'......'

def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Dict[str, Dict]:
    """
    output dictionary should be of the following format:
    {
      "2ee2b1ca-33d9-11e1-a274-61fcdeecc5f5": {
        "id": "2ee2b1ca-33d9-11e1-a274-61fcdeecc5f5",
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 1325380672000,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."
      },
      "another id": {...}
    }
    "content_str" is a new field that you need to generate. The value of "content_str" is the concatenation of
    content values that are typed as "sanitized_html" from "contents" field.
    """
    dictData = {}
    with open(wapo_jl_path) as file:
        for line in file:
            conv = json.loads(line)
            sanitized_html = " ".join([each.get("content") for each in conv.get("contents") if each.get("type") == "sanitized_html"])
            dictData.update({conv.get("id"):{"id": conv.get("id"),
                                             "title": conv.get("title"),
                                             "author": conv.get("author"),
                                             "published_date": conv.get("published_date"),
                                             "content_str":sanitized_html}})
    file.close()
    return dictData
