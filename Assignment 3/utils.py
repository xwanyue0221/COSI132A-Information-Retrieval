from typing import Dict, Union, Generator, Tuple
import functools
from datetime import datetime
import os
import json
import time
import re


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer


def get_snippet(doc_dict: Dict) -> Tuple:
    """
    id: a string object which corresponds to each document's unique id
    doc_dict: a dict object which includes all essential elements possessed by a document
    return: a tuple object which includes three elements, including document unique id, document's title, and the first 150 characters of this document content
    """
    id = doc_dict['id']
    title = doc_dict['title']
    content = doc_dict['content_str']
    return id, title, content[:150]+'......'


def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    """
    Unlike HW2, load_wapo should be an iterator in this assignment. It's more memory-efficient when you need to load each document and build the inverted index.
    At each time, load_wapo will yield a dictionary of the following format:

    {   "id": 1,
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 2011-12-31 20:37:52,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."  }

    Compared to HW2, you should also make the following changes:
    - replace the original value of the key "id" with an integer that corresponds to the order of each document
      that has been loaded. For example. the id of the first yielded document is 0 and the second is 1 and so on. (done)
    - remove any HTML elements from the content_str. (done)
    - convert the value of "published_date" to a readable format. (done)
      This one is given as follows, so just sure you apply it in your implementation
            %: from datetime import datetime
            %: doc["published_date"] = datetime.fromtimestamp(doc["published_date"] / 1000.0)

    :param wapo_jl_path:
    :return: a generator which includes a dict object
    """
    counter = 0
    CLEANR = re.compile('<.*?>')
    with open(wapo_jl_path) as file:
        for line in file:
            dictData = {}
            conv = json.loads(line)
            sanitized_html = " ".join([each.get("content") for each in conv.get("contents") if each.get("type") == "sanitized_html"])
            cleantext = re.sub(CLEANR, '', sanitized_html)

            ts = int(conv.get("published_date"))/1000
            date=datetime.fromtimestamp(ts)

            dictData["id"] = counter
            dictData["title"] = conv.get("title")
            dictData["author"] = conv.get("author")
            dictData["published_date"] = date
            dictData["content_str"] = cleantext
            counter += 1

            yield dictData


if __name__ == "__main__":
    pass
